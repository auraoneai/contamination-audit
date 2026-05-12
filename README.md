# contamination-audit

`contamination-audit` combines n-gram overlap, optional embedding similarity, canary matching, answer-pattern checks, and public-corpus hash matching.

## Quickstart

```bash
pip install contamination-audit
contamination-audit run --eval-data examples/eval.jsonl --corpora pile,c4,hf-mmlu
```

## What This Is Not

Not proof of uncontaminated data; it is a code-only diagnostic. Examples are synthetic.
