import re
PATTERN=re.compile(r"\b(the\s+answer\s+is|answer:)\s*\(?[A-E]\)?", re.I)
def detect(items): return [{"detector":"answer_pattern","item_id":i.get('item_id'),"match":PATTERN.search(i.get('text', i.get('prompt',''))).group(0)} for i in items if PATTERN.search(i.get('text', i.get('prompt','')))]
