def risk_score(findings): return min(1.0, len(findings)/10)
def build(findings, item_count): return {"item_count": item_count, "finding_count": len(findings), "aggregate_risk_score": risk_score(findings), "findings": findings, "synthetic": True, "reproducible": True}
