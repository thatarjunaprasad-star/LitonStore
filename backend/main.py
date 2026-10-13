from __future__ import annotations
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from .scraper import scrape_all_sites
from .agent import bulk_upsert_products
from .search import search_products

load_dotenv()

log = logging.getLogger(__name__)

app = FastAPI(title="Liton Tea Store API")

class ScrapeResponse(BaseModel):
    message: str
    items_scraped: int

class QueryRequest(BaseModel):
    question: str
    top_k: int = 5

class QueryResult(BaseModel):
    name: str
    price: str | None = None
    url: str | None = None
    score: float

class QueryResponse(BaseModel):
    results: list[QueryResult]

@app.post("/scrape", response_model=ScrapeResponse)
def trigger_scrape():
    """Scrape supported e‑commerce sites and store data in SQLite."""
    try:
        items = scrape_all_sites()
        if not items:
            raise HTTPException(status_code=500, detail="No items scraped")
        # Prepare dicts for DB upsert (match keys used in bulk_upsert_products)
        records = [
            {
                "name": i.get("name"),
                "price": i.get("price"),
                "url": i.get("url"),
                "description": i.get("description"),
            }
            for i in items
        ]
        bulk_upsert_products(records)
        return ScrapeResponse(message="Scrape completed", items_scraped=len(items))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
def ask_question(request: QueryRequest):
    """Answer a natural‑language question by performing a simple TF‑IDF search.

    The function returns the top‑k most similar products.
    """
    try:
        results = search_products(request.question, top_k=request.top_k)
        formatted = [
            QueryResult(
                name=prod.name,
                price=prod.price,
                url=prod.url,
                score=score,
            )
            for prod, score in results
        ]
        return QueryResponse(results=formatted)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
