import json
import urllib.error
import urllib.request

from openhip.settings import settings


def to_observation_resource(target_code: str, value: float, unit: str, patient_id: str) -> dict:
    return {
        "resourceType": "Observation",
        "status": "final",
        "code": {"coding": [{"system": "http://loinc.org/demo", "code": target_code}]},
        "subject": {"reference": f"Patient/{patient_id}"},
        "valueQuantity": {"value": value, "unit": unit},
    }


def push_observation(resource: dict) -> bool:
    """Best-effort POST to a local HAPI FHIR server. Off unless OPENHIP_FHIR_PUSH=true."""
    if not settings.fhir_push:
        return False
    url = settings.hapi_fhir_url.rstrip("/") + "/Observation"
    request = urllib.request.Request(
        url,
        data=json.dumps(resource).encode("utf-8"),
        headers={"Content-Type": "application/fhir+json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=3) as response:
            return response.status in (200, 201)
    except (urllib.error.URLError, OSError):
        return False
