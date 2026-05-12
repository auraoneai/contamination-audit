# contamination-audit

`contamination-audit` combines n-gram overlap, optional embedding similarity, canary matching, answer-pattern checks, and public-corpus hash matching.

## Quickstart

```bash
pip install contamination-audit
contamination-audit run --eval-data examples/eval.jsonl --corpora pile,c4,hf-mmlu
```

By default, embedding checks use a no-dependency lexical cosine fallback. To run semantic embedding checks locally:

```bash
pip install 'contamination-audit[embedding]'
contamination-audit run --eval-data examples/eval.jsonl --embedding-backend sentence-transformers --embedding-model all-MiniLM-L6-v2
```

## What This Is Not

Not proof of uncontaminated data; it is a code-only diagnostic. Examples are synthetic.
