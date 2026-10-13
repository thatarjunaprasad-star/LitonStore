from __future__ import annotations
import logging
from typing import List, Dict
from sqlalchemy.orm import Session
from .models import Product, get_engine, get_sessionmaker

log = logging.getLogger(__name__)

# ----------------------------------------------------------------------
# Database setup (SQLite)
# ----------------------------------------------------------------------
engine = get_engine()
SessionLocal = get_sessionmaker(engine)


def get_db() -> Session:
    """Utility to obtain a SQLAlchemy session (for FastAPI dependencies)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def bulk_upsert_products(items: List[Dict[str, str]]) -> int:
    """Insert or update scraped product records.

    *items* is a list of dictionaries with keys ``name``, ``price``, ``url``,
    optionally ``description``.  The function matches on ``url`` (or ``name``
    when ``url`` is missing) and updates existing rows; otherwise it inserts a
    new one.
    """
    count = 0
    with SessionLocal() as db:
        for it in items:
            query = db.query(Product)
            if it.get("url"):
                query = query.filter(Product.url == it["url"]).filter(Product.url != None)  # noqa: E711
            else:
                query = query.filter(Product.name == it["name"]).filter(Product.name != None)  # noqa: E711
            existing = query.first()
            if existing:
                existing.name = it["name"]
                existing.price = it.get("price")
                existing.description = it.get("description")
                existing.url = it.get("url")
            else:
                prod = Product(
                    name=it["name"],
                    price=it.get("price"),
                    url=it.get("url"),
                    description=it.get("description"),
                )
                db.add(prod)
            count += 1
        db.commit()
    log.info("✅ %d product records upserted", count)
    return count
