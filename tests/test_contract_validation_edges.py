from datetime import UTC, datetime, timedelta

from openhip.contracts import load_contract, validate_structure
from openhip.pipeline import build_oru_payload, parse_oru


def _parsed(**overrides: str) -> dict[str, str]:
    parsed = parse_oru(build_oru_payload(1))
    parsed.update(overrides)
    return parsed


def test_contract_rejects_non_oru_message_type():
    contract = load_contract("oru_contract")
    result = validate_structure(_parsed(message_type="ADT"), contract)

    assert result is not None
    assert result[1] == "ORU.MESSAGE.TYPE"


def test_contract_rejects_bad_decimal_observation_value():
    contract = load_contract("oru_contract")
    result = validate_structure(_parsed(observation_value="not-a-number"), contract)

    assert result is not None
    assert result[1] == "ORU.OBSERVATION.VALUE.DECIMAL"


def test_contract_rejects_invalid_observation_datetime():
    contract = load_contract("oru_contract")
    result = validate_structure(_parsed(observation_datetime="not-a-date"), contract)

    assert result is not None
    assert result[1] == "ORU.OBSERVATION.DATETIME.DATETIME"


def test_contract_rejects_future_observation_datetime():
    future = (datetime.now(UTC) + timedelta(days=1)).isoformat()
    contract = load_contract("oru_contract")
    result = validate_structure(_parsed(observation_datetime=future), contract)

    assert result is not None
    assert result[1] == "ORU.OBS.DATETIME.NOT_FUTURE"
