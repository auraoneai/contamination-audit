# contamination-audit

**Benchmark contamination scanner.** Generate item-level signals that help
reviewers investigate possible evaluation-data leakage.

[![PyPI](https://img.shields.io/pypi/v/contamination-audit)](https://pypi.org/project/contamination-audit/)
[![CI](https://github.com/auraoneai/contamination-audit/actions/workflows/ci.yml/badge.svg)](https://github.com/auraoneai/contamination-audit/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](https://github.com/auraoneai/contamination-audit/blob/main/LICENSE)

From a source checkout:

```bash
python -m pip install contamination-audit==0.1.2
contamination-audit run --eval-data examples/eval.jsonl --skip-embedding
```

Output on the bundled synthetic eval file (exit code `0`):

```json
{
  "item_count": 2,
  "finding_count": 1,
  "aggregate_risk_score": 0.1,
  "findings": [
    {
      "detector": "answer_pattern",
      "item_id": "1",
      "match": "The answer is (B)"
    }
  ],
  "synthetic": true,
  "reproducible": true
}
```

## What It Does and Doesn't Do

It does:

- run n-gram overlap, answer-pattern, canary, registry-hash, lexical
  similarity, and optional sentence-transformers checks locally;
- report every detector-level finding with item ids and matched evidence.

It doesn't:

- prove contamination or cleanliness. Findings are risk signals for a reviewer
  to investigate;
- download or search real corpora. The built-in `pile`, `c4`, and `hf-mmlu`
  registry entries are synthetic marker hashes.

Part of the AuraOne review quality workflow:
[judge-bench](https://auraone.ai/open/judge-bench) →
[evalkit](https://auraone.ai/open/evalkit).
Project page: [auraone.ai/open/contamination-audit](https://auraone.ai/open/contamination-audit).

## Overview

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

---

Need an independent model-quality evaluation or benchmark program?
[Talk to AuraOne](https://auraone.ai/contact?from=open:contamination-audit)
