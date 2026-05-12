def cosine_bow(a: str, b: str):
    sa=set(a.lower().split()); sb=set(b.lower().split()); return len(sa&sb)/((len(sa)*len(sb))**0.5) if sa and sb else 0.0
def detect(items, references=None, threshold=0.8):
    findings=[]
    for item in items:
        for ref in references or []:
            score=cosine_bow(item.get('text', item.get('prompt','')), ref.get('text', ref.get('prompt','')))
            if score>=threshold: findings.append({"detector":"embedding","item_id":item.get('item_id'),"reference_id":ref.get('item_id'),"score":round(score,6),"optional_dependency":"sentence-transformers-compatible"})
    return findings
