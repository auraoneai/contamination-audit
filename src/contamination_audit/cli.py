import argparse,json
from pathlib import Path
from .detectors import ngram, canary, answer_pattern, public_corpus
from .corpora.registry import REGISTRY
from .report import build

def load(path): return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]
def run(items):
    findings=[]; findings += ngram.detect(items); findings += answer_pattern.detect(items); findings += public_corpus.detect(items, REGISTRY); findings += canary.detect(items, [])
    return build(findings, len(items))
def main(argv=None):
    p=argparse.ArgumentParser(prog="contamination-audit"); sub=p.add_subparsers(dest="cmd", required=True); r=sub.add_parser("run"); r.add_argument("--eval-data", required=True); r.add_argument("--corpora", default="pile,c4,hf-mmlu")
    args=p.parse_args(argv); print(json.dumps(run(load(args.eval_data)), indent=2)); return 0
if __name__ == "__main__": raise SystemExit(main())
