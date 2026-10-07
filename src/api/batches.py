import csv
import io
import logging
from datetime import UTC, datetime, timedelta
from typing import Annotated, Any, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi import Query as FastQuery
from postgrest.exceptions import APIError
from supabase_auth.errors import AuthApiError

from src.api.auth import Actor, current_user, role_of, supabase_client
from src.api.campaign import (
    audit,
    deliver,
    verified_body,
    webhook_configured,
    webhook_payload,
)
from src.api.schemas import (
    AuditEntry,
    AuditRole,
    Batch,
    BatchStatus,
    CreateBatchRequest,
    DecisionRequest,
    DeliveryResult,
    ExportBatchResponse,
    LockedWallet,
    LockReason,
    LoginRequest,
    LoginResponse,
    Receipt,
    SmsStatus,
    UserRole,
)
from src.rules.remedies import REMEDIES
from supabase import Client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api")

SB = Annotated[Client, Depends(supabase_client)]
User = Annotated[Actor, Depends(current_user)]

# Postgres error codes raised by the migration's functions/constraints -> HTTP.
DB_ERRORS = {
    "23505": (409, "A wallet is already in an open batch"),
    "P0002": (404, "Batch not found"),
    "55000": (409, "Batch is not in 'proposed' state"),
    "42501": (403, "You cannot decide a batch you proposed"),
    "P0004": (409, "A wallet was approved in a campaign in the last 30 days"),
    "P0005": (429, "Too many open batches. Wait for a decision before proposing more."),
}


def _rpc(sb: Client, fn: str, params: dict) -> Any:
    try:
        return sb.rpc(fn, params).execute().data
    except APIError as exc:
        if exc.code in DB_ERRORS:
            status, detail = DB_ERRORS[exc.code]
            raise HTTPException(status, detail) from exc
        raise


def _batch(row: Any) -> Batch:
    return Batch(
        id=str(row["id"]),
        cause=row["cause"],
        remedy_code=row["remedy_code"],
        unit_cost_bdt=row["unit_cost_paisa"] / 100,
        wallet_count=row["wallet_count"],
        status=row["status"],
        proposed_by=str(row["proposed_by"]),
        decided_by=row["decided_by"],
        decided_at=row["decided_at"],
        decision_note=row["decision_note"],
        created_at=row["created_at"],
    )


CAMPAIGN_ACTIONS = ["campaign.delivered", "campaign.failed", "campaign.receipt"]


def _with_sms(sb: Client, batches: list[Batch]) -> list[Batch]:
    """Attach each approved batch's SMS hand-off state (latest webhook attempt, latest receipt)."""
    ids = [b.id for b in batches if b.status == BatchStatus.approved]
    if not ids:
        return batches
    sms = {i: SmsStatus(gateway_connected=webhook_configured()) for i in ids}
    try:
        events: Any = (sb.table("audit_log").select("action, target_id, metadata, created_at")
                       .in_("target_id", ids).in_("action", CAMPAIGN_ACTIONS).order("created_at").execute().data)
    except APIError as exc:
        logger.warning("Failed to read campaign events: %s", exc)
        events = []
    for e in events:
        s, m = sms[str(e["target_id"])], e.get("metadata") or {}
        if e["action"] == "campaign.receipt":
            s.sent, s.delivered, s.failed = m.get("sent"), m.get("delivered"), m.get("failed")
            s.failed_wallet_ids = m.get("failed_wallet_ids") or []
        else:
            s.webhook = "delivered" if e["action"] == "campaign.delivered" else "failed"
    return [b.model_copy(update={"sms": sms.get(b.id)}) for b in batches]


def _require(actor: Actor, role: UserRole) -> None:
    if actor.role != role:
        raise HTTPException(403, f"Requires the {role.value} role")


@router.post("/auth/login", response_model=LoginResponse)
def login(req: LoginRequest, sb: SB) -> LoginResponse:
    # Authenticate with Supabase credentials and return JWT access token and user role
    try:
        resp = sb.auth.sign_in_with_password({"email": req.email, "password": req.password})
    except AuthApiError as exc:
        raise HTTPException(401, "Invalid email or password") from exc
    except Exception as exc:
        logger.warning("Supabase login failed: %s", exc)
        raise HTTPException(503, "Write path offline") from exc
    if not resp.session or not resp.user:
        raise HTTPException(401, "Invalid email or password")
    return LoginResponse(
        access_token=resp.session.access_token,
        user_id=resp.user.id,
        role=role_of(resp.user.app_metadata),
    )


@router.get("/batches", response_model=list[Batch])
def list_batches(
    sb: SB,
    status: BatchStatus | None = None,
    limit: int = FastQuery(20, ge=1, le=100),
    offset: int = FastQuery(0, ge=0),
) -> list[Batch]:
    # List all proposed, approved, and rejected batches with optional filtering/pagination
    query = sb.table("batch_summaries").select("*").order("created_at", desc=True)
    if status is not None:
        query = query.eq("status", status.value)
    rows: Any = query.range(offset, offset + limit - 1).execute().data
    return _with_sms(sb, [_batch(r) for r in rows])


@router.post("/batches", response_model=Batch)
def create_batch(req: CreateBatchRequest, sb: SB, actor: User) -> Batch:
    # Propose a new cause-targeted batch (Analyst only). Remedy and pricing derived from rules
    _require(actor, UserRole.analyst)
    remedy = REMEDIES[req.cause.value]
    row: Any = _rpc(
        sb,
        "propose_batch",
        {
            "p_actor": actor.id,
            "p_cause": req.cause.value,
            "p_remedy_code": remedy["remedy_code"],
            "p_unit_cost_paisa": round(remedy["unit_cost_bdt"] * 100),
            "p_wallet_ids": req.wallet_ids,
        },
    )
    return _batch(row)


def _decide(sb: Client, actor: Actor, batch_id: UUID, status: BatchStatus, note: str) -> Batch:
    _require(actor, UserRole.approver)
    row: Any = _rpc(
        sb,
        "decide_batch",
        {"p_actor": actor.id, "p_batch_id": str(batch_id), "p_status": status.value, "p_note": note},
    )
    return _batch(row)


@router.post("/batches/{id}/approve", response_model=Batch)
def approve_batch(id: UUID, req: DecisionRequest, sb: SB, actor: User) -> Batch:
    # Approve a proposed batch (Approver only, cannot approve self-proposed batches), then fire the campaign webhook
    batch = _decide(sb, actor, id, BatchStatus.approved, req.note)
    if webhook_configured():
        deliver(sb, actor.id, _export(sb, id))  # outcome goes to the audit log; never undoes the approval
    return _with_sms(sb, [batch])[0]


@router.post("/batches/{id}/reject", response_model=Batch)
def reject_batch(id: UUID, req: DecisionRequest, sb: SB, actor: User) -> Batch:
    # Reject a proposed batch (Approver only, cannot reject self-proposed batches)
    return _decide(sb, actor, id, BatchStatus.rejected, req.note)


def _export(sb: Client, id: UUID) -> ExportBatchResponse:
    rows: Any = sb.table("batch_summaries").select("*").eq("id", str(id)).execute().data
    if not rows:
        raise HTTPException(404, "Batch not found")
    b: Any = rows[0]
    if b["status"] != BatchStatus.approved.value:
        raise HTTPException(409, "Batch is not approved")
    wallets: Any = (
        sb.table("batch_wallets").select("wallet_id").eq("batch_id", str(id)).order("wallet_id").execute().data
    )
    wallet_ids = [w["wallet_id"] for w in wallets]
    return ExportBatchResponse(
        batch_id=str(b["id"]),
        cause=b["cause"],
        remedy_code=b["remedy_code"],
        wallet_ids=wallet_ids,
        cost_bdt=b["unit_cost_paisa"] * len(wallet_ids) / 100,
        approved_by=str(b["decided_by"]),
        approved_at=b["decided_at"],
    )


@router.get("/batches/{id}/export", response_model=ExportBatchResponse,
            responses={200: {"content": {"text/csv": {}}}})
def export_batch(id: UUID, sb: SB, actor: User, format: Literal["json", "csv"] = "json") -> Any:
    # Export an approved batch (Authenticated only): JSON, or CSV with one row per wallet for campaign tools
    export = _export(sb, id)
    if format == "json":
        return export
    p = webhook_payload(export)
    buf = io.StringIO()
    out = csv.writer(buf, lineterminator="\n")
    out.writerow(["batch_id", "wallet_id", "cause", "remedy_code", "unit_cost_bdt", "message_en", "message_bn"])
    unit = export.cost_bdt / len(export.wallet_ids) if export.wallet_ids else 0.0
    for w in export.wallet_ids:
        out.writerow([export.batch_id, w, export.cause.value, export.remedy_code, unit, p["message_en"], p["message_bn"]])
    return Response("\ufeff" + buf.getvalue(), media_type="text/csv; charset=utf-8",  # BOM so Excel reads Bangla
                    headers={"Content-Disposition": f'attachment; filename="campaign-{export.batch_id}.csv"'})


@router.post("/batches/{id}/redeliver", response_model=DeliveryResult)
def redeliver_batch(id: UUID, sb: SB, actor: User) -> DeliveryResult:
    # Re-send an approved batch to the campaign webhook (Approver only); receivers dedupe on Idempotency-Key
    _require(actor, UserRole.approver)
    if not webhook_configured():
        raise HTTPException(409, "Campaign webhook not configured")
    return deliver(sb, actor.id, _export(sb, id))


@router.post("/campaign/receipts", response_model=Receipt)
def campaign_receipt(receipt: Receipt, sb: SB, _body: Annotated[bytes, Depends(verified_body)]) -> Receipt:
    # SMS gateway delivery report for an approved batch, HMAC-signed with the webhook secret
    rows: Any = sb.table("batch_summaries").select("*").eq("id", str(receipt.batch_id)).execute().data
    if not rows:
        raise HTTPException(404, "Batch not found")
    if rows[0]["status"] != BatchStatus.approved.value:
        raise HTTPException(409, "Batch is not approved")
    if receipt.sent > rows[0]["wallet_count"]:
        raise HTTPException(422, "sent exceeds the batch's wallet count")
    if receipt.failed_wallet_ids:
        members: Any = sb.table("batch_wallets").select("wallet_id").eq("batch_id", str(receipt.batch_id)).execute().data
        if not set(receipt.failed_wallet_ids) <= {w["wallet_id"] for w in members}:
            raise HTTPException(422, "failed_wallet_ids contains a wallet that is not in this batch")
    meta = receipt.model_dump(mode="json", exclude={"batch_id"}, exclude_none=True)
    if not receipt.failed_wallet_ids:
        meta.pop("failed_wallet_ids")
    audit(sb, None, "system", "campaign.receipt", str(receipt.batch_id), meta)
    return receipt


@router.get("/wallets/locked", response_model=list[LockedWallet])
def list_locked_wallets(sb: SB, actor: User) -> list[LockedWallet]:
    # Returns wallets currently in an open proposed batch or within 30 days of approval
    locked_dict: dict[str, LockedWallet] = {}
    try:
        # 1. Open wallets in proposed batches
        open_rows: Any = sb.table("batch_wallets").select("wallet_id").eq("batch_status", "proposed").execute().data
        for r in open_rows:
            locked_dict[r["wallet_id"]] = LockedWallet(wallet_id=r["wallet_id"], reason=LockReason.open)

        # 2. Cooldown wallets from batches approved in last 30 days
        cutoff = (datetime.now(UTC) - timedelta(days=30)).isoformat()
        appr_batches: Any = (
            sb.table("remedy_batches")
            .select("id, decided_at")
            .eq("status", "approved")
            .gt("decided_at", cutoff)
            .execute()
            .data
        )
        if appr_batches:
            batch_ids = [b["id"] for b in appr_batches]
            batch_times = {b["id"]: b["decided_at"] for b in appr_batches}
            cooldown_wallets: Any = (
                sb.table("batch_wallets")
                .select("batch_id, wallet_id")
                .in_("batch_id", batch_ids)
                .execute()
                .data
            )
            for cw in cooldown_wallets:
                w_id = cw["wallet_id"]
                if w_id not in locked_dict:
                    d_at = batch_times.get(cw["batch_id"])
                    until_str = None
                    if d_at:
                        try:
                            d_time = datetime.fromisoformat(d_at)
                            until_str = (d_time + timedelta(days=30)).isoformat()
                        except (ValueError, TypeError):
                            until_str = None
                    locked_dict[w_id] = LockedWallet(
                        wallet_id=w_id, reason=LockReason.cooldown, until=until_str
                    )
    except APIError as exc:
        logger.warning("Failed to fetch locked wallets from Supabase: %s", exc)
    except Exception as exc:  # noqa: BLE001
        logger.warning("Unexpected error fetching locked wallets: %s", exc)

    return list(locked_dict.values())


@router.get("/batches/{id}/audit", response_model=list[AuditEntry])
def get_batch_audit(id: UUID, sb: SB, actor: User) -> list[AuditEntry]:
    # Returns the immutable audit history entries for a given batch, oldest first
    b_rows: Any = sb.table("remedy_batches").select("id").eq("id", str(id)).execute().data
    if not b_rows:
        raise HTTPException(404, "Batch not found")
    rows: Any = (
        sb.table("audit_log")
        .select("*")
        .eq("target_id", str(id))
        .order("created_at", desc=False)
        .execute()
        .data
    )
    result: list[AuditEntry] = []
    for r in rows:
        result.append(
            AuditEntry(
                id=str(r["id"]),
                actor_id=str(r["actor_id"]) if r["actor_id"] else None,
                actor_role=AuditRole(r["actor_role"]),
                action=r["action"],
                target_id=str(r["target_id"]),
                metadata=r.get("metadata") or {},
                created_at=r["created_at"],
            )
        )
    return result

