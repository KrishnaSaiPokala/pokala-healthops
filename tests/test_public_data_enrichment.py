from openhip.public_data import enrich_ordering_provider, load_provider_reference


def test_provider_reference_sample_loads():
    providers = load_provider_reference()

    assert "PRAC-0001" in providers
    assert providers["PRAC-0001"].specialty == "Pathology"


def test_provider_enrichment_returns_context_for_known_provider():
    enriched = enrich_ordering_provider("PRAC-0001")

    assert enriched["provider_reference_found"] is True
    assert enriched["provider_specialty"] == "Pathology"
    assert enriched["provider_state"] == "MD"


def test_provider_enrichment_handles_unknown_provider():
    enriched = enrich_ordering_provider("PRAC-9999")

    assert enriched == {
        "ordering_provider_id": "PRAC-9999",
        "provider_reference_found": False,
    }
