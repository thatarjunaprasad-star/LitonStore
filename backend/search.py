from __future__ import annotations
import logging
from typing import List, Tuple
import re
from collections import Counter
from .models import Product, SessionLocal

log = logging.getLogger(__name__)

def _load_products() -> List[Product]:
    with SessionLocal() as db:
        return db.query(Product).all()

def _tokenize(text: str) -> List[str]:
    # simple word tokenizer, lowercasing, remove non‑alphanum
    return re.findall(r"\b\w+\b", text.lower())

def _build_vector(tokens: List[str]) -> Counter:
    return Counter(tokens)

def _cosine_similarity(a: Counter, b: Counter) -> float:
    # Compute cosine similarity between two sparse vectors represented as Counters
    intersection = set(a) & set(b)
    dot = sum(a[t] * b[t] for t in intersection)
    norm_a = sum(v * v for v in a.values()) ** 0.5
    norm_b = sum(v * v for v in b.values()) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)

def search_products(query: str, top_k: int = 5) -> List[Tuple[Product, float]]:
    """Very light‑weight keyword similarity search.

    Returns the *top_k* products ordered by cosine similarity of token counts.
    """
    query_vec = _build_vector(_tokenize(query))
    products = _load_products()
    scores: List[Tuple[Product, float]] = []
    for prod in products:
        text = f"{prod.name or ''} {prod.description or ''}".strip()
        prod_vec = _build_vector(_tokenize(text))
        sim = _cosine_similarity(query_vec, prod_vec)
        scores.append((prod, sim))
    # Sort descending by similarity
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_k]
