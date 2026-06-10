from openhip.db import SessionLocal, reset_db
from openhip.mpi import match_patient
from openhip.pipeline import seed_reference_data


def test_mpi_tiers():
    reset_db()
    seed_reference_data()
    with SessionLocal() as db:
        assert match_patient(db, "MRN-100003").match_type == "exact_match"
        far = match_patient(db, "MRN-999999", "Totally Unrelated Name")
        assert far.match_type == "unmatched"
        assert far.review_required is True
