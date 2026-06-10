from openhip.contracts import load_contract, mapping_required, validate_structure


def test_required_field_failure():
    contract = load_contract("oru_contract")
    parsed = {"patient_mrn": "MRN-1", "observation_code": "GLU_FAST"}
    result = validate_structure(parsed, contract)
    assert result is not None
    assert result[0] == "contract_schema_failure"


def test_future_datetime_rejected():
    contract = load_contract("oru_contract")
    parsed = {f: "x" for f in contract["required_fields"]}
    parsed["observation_datetime"] = "2999-01-01T00:00:00Z"
    result = validate_structure(parsed, contract)
    assert result is not None
    assert result[1] == "ORU.OBS.DATETIME.NOT_FUTURE"


def test_mapping_required_flag():
    assert mapping_required(load_contract("oru_contract")) is True
