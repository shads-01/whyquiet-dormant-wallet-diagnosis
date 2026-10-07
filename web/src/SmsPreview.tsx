import { useEffect, useState } from "react";
import { exportBatch, type Batch } from "./api";
import { Button, Chip, Modal, Table } from "./design/ui";
import type { Remedy } from "./seed";

type WalletState = "delivered" | "failed" | "pending" | "totals-only";

const STATE_CHIP: Record<WalletState, { tone: "success" | "danger" | "neutral" | "warning"; label: string }> = {
  failed: { tone: "danger", label: "failed" },
  delivered: { tone: "success", label: "delivered" },
  pending: { tone: "neutral", label: "pending" },
  "totals-only": { tone: "warning", label: "in totals only" },
};

/** What the customer's phone shows and what happened to each wallet's SMS (D60). No phone numbers: IDs only. */
export default function SmsPreview({ batch, remedy, onClose, canRetry, sending, onRetry }: {
  batch: Batch;
  remedy: Remedy | undefined;
  onClose: () => void;
  canRetry: boolean;
  sending: boolean;
  onRetry: () => void;
}) {
  const [walletIds, setWalletIds] = useState<string[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    exportBatch(batch.id)
      .then((e) => setWalletIds(e.wallet_ids))
      .catch((err) => setError(err instanceof Error ? err.message : "Could not load the batch's wallets."));
  }, [batch.id]);

  const sms = batch.sms;
  const reported = sms?.sent != null;
  const failedIds = new Set(sms?.failed_wallet_ids ?? []);
  const itemised = reported && failedIds.size === (sms?.failed ?? 0);
  const stateOf = (id: string): WalletState =>
    !reported ? "pending" : !itemised ? "totals-only" : failedIds.has(id) ? "failed" : "delivered";
  const rows = (walletIds ?? [])
    .map((id) => ({ id, state: stateOf(id) }))
    .sort((a, b) => Number(b.state === "failed") - Number(a.state === "failed"));

  return (
    <Modal
      open
      wide
      onClose={onClose}
      title={`SMS for batch ${batch.id.slice(0, 8)} · ${remedy?.label ?? batch.remedy_code}`}
      testid="sms-preview"
      footer={
        <>
          {canRetry && (
            <Button variant="secondary" onClick={onRetry} loading={sending} data-testid="sms-preview-retry">
              Retry SMS send
            </Button>
          )}
          <Button variant="ghost" onClick={onClose}>Close</Button>
        </>
      }
    >
      <div className="grid gap-5 md:grid-cols-[220px_1fr]">
        {/* What lands on the customer's phone, exactly as sent to the gateway */}
        <figure className="mx-auto w-[220px] rounded-[28px] border-4 border-[var(--border)] bg-[var(--surface-2)] p-3 shadow-[var(--shadow-1)]" aria-label="Phone preview of the SMS">
          <div className="mb-3 flex justify-between text-[10px] font-semibold text-[var(--text-muted)]">
            <span>upay</span>
            <span>SMS</span>
          </div>
          {remedy ? (
            <div className="space-y-2 text-[12px] leading-snug text-[var(--text)]">
              <p lang="bn" className="rounded-2xl rounded-tl-sm bg-[var(--surface)] p-2.5" data-testid="sms-preview-bn">{remedy.message_bn}</p>
              <p className="rounded-2xl rounded-tl-sm bg-[var(--surface)] p-2.5" data-testid="sms-preview-en">{remedy.message_en}</p>
            </div>
          ) : (
            <p className="text-[12px]">Message text unavailable.</p>
          )}
          <figcaption className="mt-3 text-center text-[10px] text-[var(--text-faint)]">
            Phone numbers stay with upay. WhyQuiet sends wallet IDs only.
          </figcaption>
        </figure>

        {/* Delivery result per wallet */}
        <div className="min-w-0 space-y-3">
          <div className="flex flex-wrap gap-1.5 text-xs" data-testid="sms-preview-totals">
            {reported ? (
              <>
                <Chip tone="accent">{sms?.sent} sent</Chip>
                <Chip tone="success">{sms?.delivered} delivered</Chip>
                <Chip tone={sms?.failed ? "danger" : "neutral"}>{sms?.failed} failed</Chip>
              </>
            ) : (
              <Chip tone="neutral">
                {sms?.webhook === "delivered" ? "Sent to gateway, no delivery report yet" : "Not delivered to the gateway yet"}
              </Chip>
            )}
          </div>
          {reported && !itemised && (
            <p className="text-xs">The gateway reported totals without naming the failed wallets.</p>
          )}
          {error ? (
            <p role="alert" className="text-xs text-[var(--danger)]">{error}</p>
          ) : !walletIds ? (
            <p role="status" className="text-xs">Loading wallets…</p>
          ) : (
            <div className="max-h-72 overflow-auto" tabIndex={0} role="region" aria-label="SMS status per wallet">
              <Table testid="sms-preview-wallets">
                <thead>
                  <tr>
                    <th scope="col">Wallet</th>
                    <th scope="col">SMS status</th>
                  </tr>
                </thead>
                <tbody>
                  {rows.map((r) => (
                    <tr key={r.id} data-testid={`sms-wallet-${r.id}`}>
                      <th scope="row" className="font-mono">{r.id}</th>
                      <td><Chip tone={STATE_CHIP[r.state].tone}>{STATE_CHIP[r.state].label}</Chip></td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            </div>
          )}
        </div>
      </div>
    </Modal>
  );
}
