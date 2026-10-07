from enum import Enum
from typing import Annotated, Literal, Self
from uuid import UUID

from pydantic import BaseModel, Field, StringConstraints, model_validator


class CauseFamily(str, Enum):
    job_exit = "job_exit"
    migration = "migration"
    solved_problem = "solved_problem"
    fee_shock = "fee_shock"
    supply_failure = "supply_failure"


class UserRole(str, Enum):
    analyst = "analyst"
    approver = "approver"


class BatchStatus(str, Enum):
    proposed = "proposed"
    approved = "approved"
    rejected = "rejected"


class StoreKind(str, Enum):
    local = "local"
    supabase = "supabase"


class HealthResponse(BaseModel):
    status: str
    version: str
    store: StoreKind
    stub: bool = False
    model_version: str | None = None  # None when the scoring model file is missing


# Write-path models (docs/contracts/api.md)

WalletIdStr = Annotated[str, StringConstraints(pattern=r"^W-[0-9A-Z]{6}$")]


class LoginRequest(BaseModel):
    # Credentials for Supabase password-based authentication
    email: str
    password: str


class LoginResponse(BaseModel):
    # JWT access token and user metadata returned upon successful login
    access_token: str
    user_id: str
    role: UserRole


class SmsStatus(BaseModel):
    # Campaign hand-off state of an approved batch, folded from campaign.* audit rows (D55)
    gateway_connected: bool  # CAMPAIGN_WEBHOOK_URL + secret set on this server
    webhook: Literal["delivered", "failed"] | None = None  # latest delivery attempt; None = never sent
    sent: int | None = None  # latest gateway receipt
    delivered: int | None = None
    failed: int | None = None
    failed_wallet_ids: list[str] = Field(default_factory=list)  # which wallets the gateway could not reach


class Batch(BaseModel):
    # Batch representation matching the frontend contract (docs/contracts/api.md)
    id: str
    cause: CauseFamily
    remedy_code: str
    unit_cost_bdt: float
    wallet_count: int
    status: BatchStatus
    proposed_by: str
    decided_by: str | None = None
    decided_at: str | None = None
    decision_note: str | None = None
    created_at: str
    sms: SmsStatus | None = None  # approved batches only


class CreateBatchRequest(BaseModel):
    # Proposal payload from an analyst. Wallet IDs must match ^W-[0-9A-Z]{6}$ (1..1000 items)
    cause: CauseFamily
    wallet_ids: list[WalletIdStr] = Field(..., min_length=1, max_length=1000)


class DecisionRequest(BaseModel):
    # Approver decision payload with mandatory audit note (1..500 characters)
    note: Annotated[str, StringConstraints(min_length=1, max_length=500, strip_whitespace=True)]


class ExportBatchResponse(BaseModel):
    # Export payload containing approved campaign remedy parameters and target wallets
    batch_id: str
    cause: CauseFamily
    remedy_code: str
    wallet_ids: list[str]
    cost_bdt: float
    approved_by: str
    approved_at: str


class LockReason(str, Enum):
    open = "open"
    cooldown = "cooldown"


class LockedWallet(BaseModel):
    # Wallet locked due to an open batch or 30-day post-approval cooldown
    wallet_id: str
    reason: LockReason
    until: str | None = None


class AuditRole(str, Enum):
    analyst = "analyst"
    approver = "approver"
    system = "system"  # SMS gateway receipts (D53)


class AuditEntry(BaseModel):
    # Immutable audit trail entry
    id: str
    actor_id: str | None = None
    actor_role: AuditRole
    action: str
    target_id: str
    metadata: dict[str, str | int | float | bool | list[str] | None] = Field(default_factory=dict)
    created_at: str


# Live scoring (docs/contracts/ingest.md, D52)


class PayCycle(str, Enum):
    weekly = "weekly"
    biweekly = "biweekly"
    monthly = "monthly"


class WeekRow(BaseModel):
    # One wallet-week of ledger aggregates. Week 0..51 of the 52-week window ending at the scoring date.
    week: int = Field(..., ge=0, le=51)
    txn_count: int = Field(..., ge=0)
    amount_bdt: float = Field(..., ge=0)
    cashin_count: int = Field(0, ge=0)
    cashout_ok: int = Field(0, ge=0)
    cashout_fail: int = Field(0, ge=0)
    app_share: float | None = Field(None, ge=0, le=1)  # share of transactions made in the app; null if none
    district_changed: bool = False


class WalletHistory(BaseModel):
    # A wallet's header plus its weekly rows. Missing weeks count as silent (all zeros).
    wallet_id: WalletIdStr
    acquired_week: int = Field(..., ge=0, le=51)
    fee_week: int = Field(..., ge=0, le=51)  # week the last fee change reached this wallet
    pay_cycle: PayCycle
    weeks: list[WeekRow] = Field(..., min_length=1, max_length=52)

    @model_validator(mode="after")
    def _weeks_fit(self) -> Self:
        seen = [w.week for w in self.weeks]
        if len(set(seen)) != len(seen):
            raise ValueError("duplicate week")
        if min(seen) < self.acquired_week:
            raise ValueError("week before acquired_week")
        return self


class ScoreRequest(BaseModel):
    wallets: list[WalletHistory] = Field(..., min_length=1, max_length=500)

    @model_validator(mode="after")
    def _unique_ids(self) -> Self:
        if len({w.wallet_id for w in self.wallets}) != len(self.wallets):
            raise ValueError("duplicate wallet_id")
        return self


class Contribution(BaseModel):
    feature: str
    value: float
    contribution: float


class RuleBaseline(BaseModel):
    fired: bool
    action: str


class Remedy(BaseModel):
    remedy_code: str
    label: str
    unit_cost_bdt: float


class ScoreResult(BaseModel):
    wallet_id: str
    weeks_silent: int
    verdict: Literal["attributed", "refused"]
    cause: CauseFamily | None
    posterior: dict[str, float]  # empty when refused before the model (not dormant, no history)
    contributions: list[Contribution]
    refusal_reasons: list[str]
    rule_baseline: RuleBaseline
    remedy: Remedy | None


class ScoreResponse(BaseModel):
    model_version: str
    tau: float
    delta: float
    results: list[ScoreResult]


# Campaign webhook and SMS gateway receipts (D53)


class DeliveryResult(BaseModel):
    delivered: bool
    status_code: int | None = None
    error: str | None = None


class Receipt(BaseModel):
    # Delivery report the SMS gateway posts back for one approved batch, signed like the webhook
    batch_id: UUID
    sent: int = Field(..., ge=0)
    delivered: int = Field(..., ge=0)
    failed: int = Field(..., ge=0)
    gateway_ref: Annotated[str, StringConstraints(max_length=100)] | None = None
    failed_wallet_ids: list[WalletIdStr] = Field(default_factory=list, max_length=1000)  # optional detail (D56)

    @model_validator(mode="after")
    def _counts_add_up(self) -> Self:
        if self.delivered + self.failed > self.sent:
            raise ValueError("delivered + failed exceeds sent")
        ids = self.failed_wallet_ids
        if ids and (len(ids) != self.failed or len(set(ids)) != len(ids)):
            raise ValueError("failed_wallet_ids must list each failed wallet exactly once")
        return self
