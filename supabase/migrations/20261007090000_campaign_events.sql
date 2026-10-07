-- Campaign webhook deliveries and SMS-gateway receipts in the append-only audit log (D56).
-- Only loosens checks, so every existing row stays valid and the live code keeps working (D51).
--   campaign.delivered / campaign.failed: the approver whose approve or redeliver call fired the webhook
--   campaign.receipt: posted by the SMS gateway (HMAC-signed), so no user; actor_role 'system', actor_id null

alter table public.audit_log alter column actor_id drop not null;

alter table public.audit_log drop constraint audit_log_actor_role_check;
alter table public.audit_log add constraint audit_log_actor_role_check
  check (actor_role in ('analyst','approver','system'));

alter table public.audit_log drop constraint audit_log_action_check;
alter table public.audit_log add constraint audit_log_action_check
  check (action in ('batch.propose','batch.approve','batch.reject',
                    'campaign.delivered','campaign.failed','campaign.receipt'));

alter table public.audit_log drop constraint audit_log_role_matches_action;
alter table public.audit_log add constraint audit_log_role_matches_action check (
  (action = 'batch.propose' and actor_role = 'analyst')
  or (action in ('batch.approve','batch.reject','campaign.delivered','campaign.failed') and actor_role = 'approver')
  or (action = 'campaign.receipt' and actor_role = 'system')
);

alter table public.audit_log add constraint audit_log_system_has_no_actor
  check ((actor_role = 'system') = (actor_id is null));
