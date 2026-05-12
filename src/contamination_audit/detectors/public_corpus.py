def detect(items, registry):
    hashes={v['hash']: name for name,v in registry.items()}; return [{"detector":"public_corpus","item_id":i.get('item_id'),"corpus":hashes[i.get('hash')]} for i in items if i.get('hash') in hashes]
