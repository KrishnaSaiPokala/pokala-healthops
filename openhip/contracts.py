from datetime import UTC, datetime
from functools import lru_cache
from pathlib import Path

import yaml

CONTRACTS_DIR = Path(__file__).resolve().parent.parent / "contracts"


@lru_cache(maxsize=8)
def load_contract(name: str) -> dict:
    path = CONTRACTS_DIR / f"{name}.yml"
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _is_future(value: str) -> bool:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed > datetime.now(UTC)


def validate_structure(parsed: dict, contract: dict) -> tuple[str, str, str] | None:
    """Return (category, rule_id, error) for the first structural failure, else None."""
    for field in contract.get("required_fields", []):
        if not parsed.get(field):
            return (
                "contract_schema_failure",
                f"ORU.REQUIRED.{field.upper()}",
                f"{field} is required",
            )

    rules = contract.get("field_rules", {})
    dt_rule = rules.get("observation_datetime", {})
    if dt_rule.get("cannot_be_future") and _is_future(parsed.get("observation_datetime", "")):
        return (
            "temporal_failure",
            "ORU.OBS.DATETIME.NOT_FUTURE",
            "observation_datetime cannot be in the future",
        )
    return None


def mapping_required(contract: dict) -> bool:
    return bool(contract.get("field_rules", {}).get("observation_code", {}).get("mapping_required"))
