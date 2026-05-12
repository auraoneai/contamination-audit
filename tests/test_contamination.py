import json

from contamination_audit.cli import main, run, select_registry
from contamination_audit.detectors import answer_pattern, canary, embedding, ngram, public_corpus


def test_ngram_detector_positive_and_negative():
    items = [{"item_id": "eval", "prompt": "alpha beta gamma delta epsilon"}]
    refs = [
        {"item_id": "near", "prompt": "alpha beta gamma delta epsilon"},
        {"item_id": "far", "prompt": "zeta eta theta iota kappa"},
    ]

    findings = ngram.detect(items, refs, threshold=0.7)

    assert any(f["reference_id"] == "near" for f in findings)
    assert not any(f["reference_id"] == "far" for f in findings)


def test_embedding_detector_positive_and_negative():
    items = [{"item_id": "eval", "prompt": "robot arm opens drawer"}]
    refs = [
        {"item_id": "similar", "prompt": "robot arm opens drawer"},
        {"item_id": "different", "prompt": "invoice policy renewal"},
    ]

    findings = embedding.detect(items, refs, threshold=0.8)

    assert any(f["reference_id"] == "similar" for f in findings)
    assert not any(f["reference_id"] == "different" for f in findings)
    assert {f["backend"] for f in findings} == {"lexical-bow"}


def test_embedding_detector_sentence_transformers_backend_with_injected_model():
    class FakeSentenceTransformer:
        def encode(self, texts, normalize_embeddings=True):
            assert normalize_embeddings is True
            vectors = {
                "robot arm opens drawer": [1.0, 0.0],
                "manipulator opens cabinet": [0.95, 0.05],
                "invoice policy renewal": [0.0, 1.0],
            }
            return [vectors[text] for text in texts]

    items = [{"item_id": "eval", "prompt": "robot arm opens drawer"}]
    refs = [
        {"item_id": "semantic", "prompt": "manipulator opens cabinet"},
        {"item_id": "different", "prompt": "invoice policy renewal"},
    ]

    findings = embedding.detect(items, refs, threshold=0.9, backend="sentence-transformers", model=FakeSentenceTransformer())

    assert findings == [
        {
            "detector": "embedding",
            "item_id": "eval",
            "reference_id": "semantic",
            "score": 0.998618,
            "backend": "sentence-transformers",
        }
    ]


def test_canary_detector_positive_and_negative():
    items = canary.inject([{"item_id": "a"}, {"item_id": "b"}], prefix="TEST_CANARY")

    findings = canary.detect(items, [{"output": "model leaked TEST_CANARY_0001"}])

    assert findings == [{"detector": "canary", "item_id": "b", "canary": "TEST_CANARY_0001"}]
    assert canary.detect(items, [{"output": "no leak"}]) == []


def test_answer_pattern_detector_positive_and_negative():
    items = [
        {"item_id": "leak", "prompt": "The answer is (B) because..."},
        {"item_id": "clean", "prompt": "Choose the best explanation."},
    ]

    findings = answer_pattern.detect(items)

    assert [f["item_id"] for f in findings] == ["leak"]


def test_public_corpus_detector_positive_and_negative():
    registry = {"hf-mmlu": {"hash": "abc123"}}
    items = [{"item_id": "hit", "hash": "abc123"}, {"item_id": "miss", "hash": "zzz"}]

    findings = public_corpus.detect(items, registry)

    assert findings == [{"detector": "public_corpus", "item_id": "hit", "corpus": "hf-mmlu"}]


def test_combined_run_is_reproducible_and_item_level():
    items = [
        {"item_id": "1", "prompt": "the answer is (B)", "hash": "abc123", "canary": "AURAONE_CANARY_0001"},
        {"item_id": "2", "prompt": "the answer is (B)"},
    ]
    references = [{"item_id": "ref", "prompt": "the answer is (B)"}]
    outputs = [{"output": "AURAONE_CANARY_0001"}]
    registry = {"hf-mmlu": {"hash": "abc123"}}

    first = run(items, references=references, outputs=outputs, registry=registry)
    second = run(items, references=references, outputs=outputs, registry=registry)

    assert first == second
    assert first["item_count"] == 2
    detectors = {f["detector"] for f in first["findings"]}
    assert {"ngram", "embedding", "answer_pattern", "public_corpus", "canary"} <= detectors


def test_corpora_filter_limits_public_corpus_registry():
    registry = {"hf-mmlu": {"hash": "abc123"}, "c4": {"hash": "c4hash"}}
    items = [{"item_id": "hit", "hash": "abc123"}, {"item_id": "filtered", "hash": "c4hash"}]

    report = run(items, registry=registry, corpora="hf-mmlu", include_embedding=False)

    assert select_registry(registry, "hf-mmlu") == {"hf-mmlu": {"hash": "abc123"}}
    assert [finding["item_id"] for finding in report["findings"]] == ["hit"]


def test_cli_run_smoke(tmp_path, capsys):
    data = tmp_path / "eval.jsonl"
    data.write_text(json.dumps({"item_id": "1", "prompt": "the answer is (C)"}) + "\n", encoding="utf-8")

    assert main(["run", "--eval-data", str(data)]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["finding_count"] >= 1
