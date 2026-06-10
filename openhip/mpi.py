from dataclasses import dataclass

from rapidfuzz import fuzz
from sqlalchemy import select

from openhip.models import Patient


@dataclass
class MatchResult:
    patient_id: str | None
    match_type: str
    confidence: float
    review_required: bool


def match_patient(db, mrn: str, name: str = "", dob: str = "", zip3: str = "") -> MatchResult:
    """Demonstration MPI: deterministic MRN match, then fuzzy demographic tiers."""
    exact = db.scalar(select(Patient).where(Patient.mrn == mrn))
    if exact is not None:
        return MatchResult(exact.patient_id, "exact_match", 1.0, False)

    best: Patient | None = None
    best_score = 0.0
    for candidate in db.scalars(select(Patient)).all():
        score = fuzz.token_sort_ratio(name or "", candidate.name) / 100.0
        same_dob = bool(dob) and candidate.dob == dob
        same_zip = bool(zip3) and candidate.zip3 == zip3
        weighted = score + (0.05 if same_dob else 0.0) + (0.03 if same_zip else 0.0)
        if weighted > best_score:
            best_score, best = weighted, candidate

    if best is not None and best_score >= 0.92:
        return MatchResult(best.patient_id, "probable_match", round(best_score, 2), False)
    if best is not None and best_score >= 0.80:
        return MatchResult(best.patient_id, "possible_duplicate", round(best_score, 2), True)
    return MatchResult(None, "unmatched", round(best_score, 2), True)
