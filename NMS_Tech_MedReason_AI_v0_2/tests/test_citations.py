from app.services.citations import validate_citations

def test_invalid_citation_removed():
    answer,invalid=validate_citations("Evidence [FAKE-123] and [NMS-CORE-2026]",["NMS-CORE-2026"])
    assert "FAKE-123" in invalid and "[FAKE-123]" not in answer
