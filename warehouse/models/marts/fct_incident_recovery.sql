select
  incident_id,
  recovery_state,
  inbound_messages,
  failed_messages,
  replayed_messages,
  open_dlq,
  warehouse_checks_passed,
  duplicate_observations,
  case
    when open_dlq = 0
      and duplicate_observations = 0
      and warehouse_checks_passed = 3
      and recovery_state = 'remediated'
    then true
    else false
  end as closure_ready
from {{ ref('incident_recovery_seed') }}
