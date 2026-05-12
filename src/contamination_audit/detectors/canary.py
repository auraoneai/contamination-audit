def inject(items, prefix="AURAONE_CANARY"):
    return [{**item, "canary": f"{prefix}_{i:04d}"} for i,item in enumerate(items)]
def detect(items, outputs=None):
    outputs=outputs or [] ; text="\n".join(str(o.get('output','')) for o in outputs); return [{"detector":"canary","item_id":i.get('item_id'),"canary":i.get('canary')} for i in items if i.get('canary') and i.get('canary') in text]
