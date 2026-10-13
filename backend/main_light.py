import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel  # keep import for type hints only; not used at runtime

from .scraper import scrape_all_sites

app = FastAPI(title="Liton Tea Store Light API (Python 3.14)")

# Simple response schemas using TypedDict (Python 3.8+). We'll keep BaseModel for backward compatibility

class ScrapeResponse(BaseModel):
    message: str
    items_scraped: int

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    source_documents: list = []

@app.post("/scrape", response_model=ScrapeResponse)
def trigger_scrape():
    """Scrape supported sites and return count. No vector store used in the light version."""
    try:
        items = scrape_all_sites()
        if not items:
            raise HTTPException(status_code=500, detail="No items scraped")
        return ScrapeResponse(message="Scrape completed", items_scraped=len(items))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
def ask_question(request: QueryRequest):
    """Return a placeholder answer – the full RAG chain requires heavy deps not available in this lightweight build."""
    # For demonstration we simply echo the question.
    answer = f"(Light version) You asked: '{request.question}'. Price‑related answers are not available without the full RAG stack."
    return QueryResponse(answer=answer)
