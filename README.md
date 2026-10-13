# Liton Tea Store Agent

**Name:** Liton Tea Store, Jhawtala, Cumilla
**Made by:** Twoptjabs

## Overview
A semantic AI agent that:
- Scrapes local Bangladeshi e‑commerce sites (e.g., daraz.com.bd, ajkerdeal.com) to collect product prices and generate bill summaries.
- Provides daily item suggestions with price estimates.
- Stores scraped data in a vector store for Retrieval‑Augmented Generation (RAG) so the LLM can answer natural‑language queries about prices, bills, and recommendations.
- Serves a simple, marketable front‑end with a Bengali‑aesthetic look (Bengali cultural photos, fonts, colors).

## Architecture
```
frontend/                # static HTML/CSS/JS (Bengali aesthetic)
backend/
│   main.py               # FastAPI entry point
│   scraper.py            # Site‑specific scrapers (requests + BeautifulSoup)
│   agent.py              # LangChain RAG chain (Chroma DB + OpenAI / local LLM)
│   models.py             # Pydantic request/response schemas
│   requirements.txt      # Python dependencies
└   .env                  # Optional API keys (e.g., OPENAI_API_KEY)
```

## Quick Start
```bash
# 1. Clone / create the project folder (already present)
cd "C:/Users/Programmer Arjuna/Downloads/Liton Tea Stall"

# 2. Create a virtual environment and install deps
python -m venv .venv
.venv\Scripts\activate   # Windows PowerShell
pip install -r backend/requirements.txt

# 3. (Optional) set LLM credentials in .env
#   OPENAI_API_KEY=your-key

# 4. Run the FastAPI server
uvicorn backend.main:app --reload

# 5. Open the front‑end in a browser
start frontend/index.html
```

## How It Works
1. **Scraping** – `scraper.py` contains functions for each supported site. They return a list of `{name, price, url}`.
2. **Ingestion** – Scraped items are embedded with an LLM embedding model and stored in a local Chroma DB.
3. **RAG** – `agent.py` builds a LangChain `RetrievalQA` chain that queries the vector store, then formats a response (bill summary, suggestions, etc.).
4. **API** – FastAPI endpoints (`/scrape`, `/query`) expose the functionality to the front‑end.
5. **Front‑end** – A minimal HTML page with Bengali fonts and placeholder cultural images displays suggestions and allows the user to ask natural‑language questions.

## Extending
- Add more scrapers for other sites by extending `scraper.py`.
- Swap the embedding model or vector DB (e.g., Pinecone, Weaviate) in `agent.py`.
- Enhance the UI with a modern framework (React, Vue) while preserving the Bengali aesthetic.

---
*This project is a starter template; adapt paths, credentials, and site‑specific selectors as needed.*
