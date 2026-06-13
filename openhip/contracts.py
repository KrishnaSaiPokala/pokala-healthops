from __future__ import annotations

from datetime import UTC, datetime
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

CONTRACTS_DIR = Path(__file__).resolve().parent.parent / "contracts"


@lru_cache(maxsize=8)
def load_contract(name: str) -> dict[str, Any]:
    path = CONTRACTS_DIR / f"{name}.yml"
    with path.open(encoding="utf-8") as handle:
        loaded = yaml.safe_load(handle)
    return loaded if isinstance(loaded, dict) else {}


def _parse_datetime(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _is_future(value: str) -> bool:
    parsed = _parse_datetime(value)
    if parsed is None:
        return False
    return parsed > datetime.now(UTC)


def _is_decimal(value: str) -> bool:
    try:
        float(value)
    except (TypeError, ValueError):
        return False
    return True


def _rule_id_for_field(field: str, suffix: str) -> str:
    normalized = field.upper().replace("_", ".")
    return f"ORU.{normalized}.{suffix}"


def validate_structure(
    parsed: dict[str, str],
    contract: dict[str, Any],
) -> tuple[str, str, str] | None:
    """Return (category, rule_id, error) for the first structural failure, else None.

    The contract file is intentionally data-driven. The implementation is still
    small, but it now enforces the rules that matter for this demo: required
    fields, message type, datetime parsing, future timestamp protection, and
    decimal observation values.
    """
    expected_message_type = contract.get("message_type")
    actual_message_type = parsed.get("message_type")
    if (
        expected_message_type
        and actual_message_type
        and actual_message_type != expected_message_type
    ):
        return (
            "contract_schema_failure",
            "ORU.MESSAGE.TYPE",
            f"message_type must be {expected_message_type}",
        )

    for field in contract.get("required_fields", []):
        if not parsed.get(field):
            return (
                "contract_schema_failure",
                f"ORU.REQUIRED.{field.upper()}",
                f"{field} is required",
            )

    rules = contract.get("field_rules", {})

    for field, rule in rules.items():
        value = parsed.get(field, "")
        rule_type = rule.get("type")

        if rule_type == "decimal" and value and not _is_decimal(value):
            return (
                "contract_schema_failure",
                _rule_id_for_field(field, "DECIMAL"),
                f"{field} must be decimal",
            )

        if rule_type == "datetime" and value:
            parsed_datetime = _parse_datetime(value)
            if parsed_datetime is None:
                return (
                    "contract_schema_failure",
                    _rule_id_for_field(field, "DATETIME"),
                    f"{field} must be ISO-8601 datetime",
                )
            if rule.get("cannot_be_future") and _is_future(value):
                return (
                    "temporal_failure",
                    "ORU.OBS.DATETIME.NOT_FUTURE",
                    f"{field} cannot be in the future",
                )

        min_length = rule.get("min_length")
        if isinstance(min_length, int) and value and len(value) < min_length:
            return (
                "contract_schema_failure",
                _rule_id_for_field(field, "MIN_LENGTH"),
                f"{field} must be at least {min_length} characters",
            )

    return None


def mapping_required(contract: dict[str, Any]) -> bool:
    return bool(contract.get("field_rules", {}).get("observation_code", {}).get("mapping_required"))
