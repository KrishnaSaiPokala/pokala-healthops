from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

DEFAULT_PROVIDER_REFERENCE = (
    Path(__file__).resolve().parent.parent / "data" / "public" / "provider_reference_sample.csv"
)


@dataclass(frozen=True)
class ProviderReference:
    provider_id: str
    display_name: str
    specialty: str
    state: str
    source: str


def load_provider_reference(
    path: str | Path = DEFAULT_PROVIDER_REFERENCE,
) -> dict[str, ProviderReference]:
    reference_path = Path(path)
    providers: dict[str, ProviderReference] = {}

    with reference_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            provider_id = row["provider_id"].strip()
            providers[provider_id] = ProviderReference(
                provider_id=provider_id,
                display_name=row["display_name"].strip(),
                specialty=row["specialty"].strip(),
                state=row["state"].strip(),
                source=row["source"].strip(),
            )

    return providers


def enrich_ordering_provider(
    ordering_provider_id: str,
    path: str | Path = DEFAULT_PROVIDER_REFERENCE,
) -> dict[str, str | bool]:
    providers = load_provider_reference(path)
    provider = providers.get(ordering_provider_id)

    if provider is None:
        return {
            "ordering_provider_id": ordering_provider_id,
            "provider_reference_found": False,
        }

    return {
        "ordering_provider_id": provider.provider_id,
        "provider_reference_found": True,
        "provider_display_name": provider.display_name,
        "provider_specialty": provider.specialty,
        "provider_state": provider.state,
        "provider_reference_source": provider.source,
    }
