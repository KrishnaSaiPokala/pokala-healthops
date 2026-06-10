import os

from pydantic import BaseModel


class Settings(BaseModel):
    env: str = os.getenv("OPENHIP_ENV", "local")
    no_phi: bool = os.getenv("OPENHIP_NO_PHI", "true").lower() == "true"
    db_url: str = os.getenv("OPENHIP_DB_URL", "sqlite:///./openhip.db")
    hapi_fhir_url: str = os.getenv("HAPI_FHIR_URL", "http://localhost:8080/fhir")
    fhir_push: bool = os.getenv("OPENHIP_FHIR_PUSH", "false").lower() == "true"


settings = Settings()
