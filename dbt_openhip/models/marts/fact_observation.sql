select
  observation_id,
  run_id,
  patient_id,
  encounter_id,
  target_code,
  value_numeric,
  unit,
  abnormal_flag
from {{ ref('stg_observation') }}
