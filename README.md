# contamination-audit

Generate item-level signals that help reviewers investigate possible evaluation-data leakage.

`contamination-audit` is for benchmark maintainers and evaluation engineers who want a local, inspectable preflight before deeper contamination analysis. It combines n-gram overlap, answer-pattern checks, canary matching, synthetic registry-hash matching, lexical similarity, and an optional sentence-transformers backend.

## Inspectable Output

The CLI writes JSON with `item_count`, `finding_count`, a bounded aggregate risk score, and every detector-level finding. Findings include item and reference ids, detector name, matched corpus marker, canary, or similarity score where applicable.

The Python `run` API accepts separate `items`, `references`, `outputs`, and registry data. The CLI currently accepts only `--eval-data`; it uses those same rows as its comparison references and does not accept model outputs, so it is a smoke-test path rather than a held-out-corpus audit.

## Runtime Boundary

The default lexical path runs locally with no network dependency. The built-in `pile`, `c4`, and `hf-mmlu` registry entries are synthetic marker hashes; the package does not download or search those corpora.

The optional `sentence-transformers` backend loads the named model locally. Its underlying library may download model files when they are not already cached, so use a local model/cache when runtime network access is not allowed.

## Install

```bash
python -m pip install contamination-audit==0.1.2
```

Optional semantic embeddings:

```bash
python -m pip install "contamination-audit[embedding]==0.1.2"
```

For development from a clone:

```bash
python -m pip install -e .
```

## Quickstart

From a repository checkout, run the no-download path:

```bash
contamination-audit run \
  --eval-data examples/eval.jsonl \
  --skip-embedding \
  > contamination-report.json
```

See [`docs/methodology.md`](docs/methodology.md) for detector and data-boundary details.

## Release Status

Registry status verified July 13, 2026: version `0.1.2` is published on PyPI and tagged `v0.1.2` in the public repository. The project is alpha software. No claim of contamination detection coverage, clean data, or adoption is made.

## Limits

This package emits diagnostic signals, not proof that data is contaminated or clean. The aggregate risk score is a simple finding-count heuristic, the bundled corpus registry is synthetic, and reviewers must interpret evidence in context.

## Next Action

Run the no-download CLI path to inspect the report shape, then call the Python API with approved, separated references and model outputs before using any finding in a contamination review.
