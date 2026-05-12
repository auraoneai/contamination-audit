import argparse,json
from pathlib import Path
from .detectors import ngram, canary, answer_pattern, embedding, public_corpus
from .corpora.registry import REGISTRY
from .report import build

def load(path): return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]
def run(items, references=None, outputs=None, registry=None, include_embedding=True):
    references = references if references is not None else items
    registry = registry if registry is not None else REGISTRY
    findings=[]
    findings += ngram.detect(items, references)
    findings += answer_pattern.detect(items)
    findings += public_corpus.detect(items, registry)
    findings += canary.detect(items, outputs or [])
    if include_embedding:
        findings += embedding.detect(items, references)
    return build(findings, len(items))
def main(argv=None):
    p=argparse.ArgumentParser(prog="contamination-audit"); sub=p.add_subparsers(dest="cmd", required=True); r=sub.add_parser("run"); r.add_argument("--eval-data", required=True); r.add_argument("--corpora", default="pile,c4,hf-mmlu")
    args=p.parse_args(argv); print(json.dumps(run(load(args.eval_data)), indent=2)); return 0
if __name__ == "__main__": raise SystemExit(main())
