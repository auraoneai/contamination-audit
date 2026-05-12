import math
import os
from typing import Any


def cosine_bow(a: str, b: str) -> float:
    sa = set(a.lower().split())
    sb = set(b.lower().split())
    return len(sa & sb) / ((len(sa) * len(sb)) ** 0.5) if sa and sb else 0.0


def detect(
    items,
    references=None,
    threshold=0.8,
    backend: str | None = None,
    model_name: str | None = None,
    model: Any | None = None,
):
    backend = (backend or os.environ.get("CONTAMINATION_AUDIT_EMBEDDING_BACKEND") or "lexical").replace("_", "-")
    references = references or []
    if backend == "sentence-transformers" or model is not None:
        return _detect_sentence_transformers(items, references, threshold, model_name, model)
    if backend != "lexical":
        raise RuntimeError(f"Unsupported embedding backend: {backend}")
    return _detect_lexical(items, references, threshold)


def _detect_lexical(items, references, threshold):
    findings = []
    for item in items:
        for ref in references:
            score = cosine_bow(_text(item), _text(ref))
            if score >= threshold:
                findings.append(_finding(item, ref, score, "lexical-bow"))
    return findings


def _detect_sentence_transformers(items, references, threshold, model_name, model):
    model = model or _load_sentence_transformer(model_name)
    item_texts = [_text(item) for item in items]
    reference_texts = [_text(ref) for ref in references]
    item_vectors = _encode(model, item_texts)
    reference_vectors = _encode(model, reference_texts)
    findings = []
    for item, item_vector in zip(items, item_vectors):
        for ref, reference_vector in zip(references, reference_vectors):
            score = _cosine(item_vector, reference_vector)
            if score >= threshold:
                findings.append(_finding(item, ref, score, "sentence-transformers"))
    return findings


def _load_sentence_transformer(model_name):
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise RuntimeError(
            "The sentence-transformers backend requires `pip install contamination-audit[embedding]` "
            "or an injected model with an encode(texts) method."
        ) from exc
    return SentenceTransformer(model_name or os.environ.get("CONTAMINATION_AUDIT_EMBEDDING_MODEL") or "all-MiniLM-L6-v2")


def _encode(model, texts):
    vectors = model.encode(texts, normalize_embeddings=True)
    return [list(vector) for vector in vectors]


def _cosine(a, b) -> float:
    dot = sum(float(x) * float(y) for x, y in zip(a, b))
    norm_a = math.sqrt(sum(float(x) * float(x) for x in a))
    norm_b = math.sqrt(sum(float(y) * float(y) for y in b))
    return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0


def _finding(item, ref, score, backend):
    return {
        "detector": "embedding",
        "item_id": item.get("item_id"),
        "reference_id": ref.get("item_id"),
        "score": round(score, 6),
        "backend": backend,
    }


def _text(payload):
    return payload.get("text", payload.get("prompt", ""))
