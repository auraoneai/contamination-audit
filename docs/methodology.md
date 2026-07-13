# Contamination Audit Methodology

`contamination-audit` is a deterministic, code-only screen for evaluation leakage. It combines lightweight detectors that can run without paid APIs and reports both item-level flags and aggregate risk.

## Detector Strategy

- N-gram overlap catches near-duplicate passages and copied prompts.
- Canary matching finds deliberately inserted strings that should not appear in model outputs or held-out artifacts.
- Answer-pattern matching catches benchmark-specific leaks such as explicit multiple-choice answer phrasing.
- Registry matching compares item-provided hashes against caller-supplied registry entries. The bundled `pile`, `c4`, and `hf-mmlu` values are synthetic marker hashes, not hashes of full public corpora.
- The embedding detector is optional because semantic similarity can be useful, but should not introduce a heavyweight runtime dependency for the default CLI path.

## CLI and API Boundary

The Python `run` API accepts distinct evaluation items, reference items, model outputs, and a registry. That is the path for a caller-controlled audit design.

The CLI currently accepts only an evaluation JSONL file. It uses those rows as both evaluation items and similarity references, and it supplies no model outputs to the canary detector. The CLI is therefore suitable for deterministic smoke testing and report-shape inspection, not a substitute for a separated reference-corpus analysis.

The package never downloads Pile, C4, MMLU, or another benchmark corpus. A caller must supply approved reference data or registry hashes through the Python API.

## Scoring

Each detector emits deterministic evidence. The report layer aggregates those findings into a reproducible risk summary without hiding the per-detector reason strings. The aggregate risk score is `min(1.0, finding_count / 10)` and is not a calibrated probability.

## Data Policy

All examples, tests, and built-in registry hashes are synthetic. The project does not bundle real customer evals, proprietary corpora, public-corpus snapshots, or paid labels.
