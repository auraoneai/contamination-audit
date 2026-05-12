from contamination_audit.cli import run

def test_synthetic_positive():
    report=run([{"item_id":"1","prompt":"the answer is (B)"},{"item_id":"2","prompt":"the answer is (B)"}])
    assert report["finding_count"] >= 1
