# Contamination Audit Methodology

`contamination-audit` is a deterministic, code-only screen for evaluation leakage. It combines lightweight detectors that can run without paid APIs and reports both item-level flags and aggregate risk.

## Detector Strategy

- N-gram overlap catches near-duplicate passages and copied prompts.
- Canary matching finds deliberately inserted strings that should not appear in model outputs or held-out artifacts.
- Answer-pattern matching catches benchmark-specific leaks such as explicit multiple-choice answer phrasing.
- Public-corpus matching compares examples against a curated registry of public benchmark hashes and names.
- The embedding detector is optional because semantic similarity can be useful, but should not introduce a heavyweight runtime dependency for the default CLI path.

## Scoring

Each detector emits deterministic evidence. The report layer aggregates those findings into a reproducible risk summary without hiding the per-detector reason strings.

## Data Policy

All examples and tests are synthetic. The project does not bundle real customer evals, proprietary corpora, or paid labels.
