import re
def ngrams(text, n=5):
    t=re.sub(r"\s+"," ",text.lower()).strip(); return {t[i:i+n] for i in range(max(len(t)-n+1,1))} if t else set()
def detect(items, references=None, threshold=0.72):
    refs=references or items; findings=[]
    for item in items:
        for ref in refs:
            if item is ref: continue
            a,b=ngrams(item.get('text', item.get('prompt',''))), ngrams(ref.get('text', ref.get('prompt','')))
            score=len(a&b)/len(a|b) if a or b else 0
            if score>=threshold: findings.append({"detector":"ngram","item_id":item.get('item_id'),"reference_id":ref.get('item_id'),"score":round(score,6)})
    return findings
