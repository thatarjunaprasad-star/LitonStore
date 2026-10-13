# run_all.ps1
# ------------------------------------------------------------
# This script sets up the Liton Tea Store backend using a simple
# SQLite store and launches the FastAPI server together with the UI.
# ------------------------------------------------------------

# 1️⃣ Activate the virtual environment
$venvPath = Join-Path $PSScriptRoot ".venv\Scripts\Activate.ps1"
if (Test-Path $venvPath) {
    . $venvPath
} else {
    Write-Error "Virtual environment not found at $venvPath"
    exit 1
}

# 2️⃣ Upgrade pip and install simplified requirements
python -m pip install --upgrade pip
python -m pip install -r backend\requirements_simple.txt

# 3️⃣ Create the SQLite database (if not already created)
python -c "from backend.models import Base, get_engine; Base.metadata.create_all(get_engine())"

# 4️⃣ Scrape product data and store it in the DB
python -c "import backend.scraper as s; s.scrape_all_sites();"

# 5️⃣ Launch the FastAPI server in a separate window (non‑blocking)
Start-Process -FilePath "python" -ArgumentList "-m", "uvicorn", "backend.main:app", "--reload" -WorkingDirectory $PSScriptRoot

# 6️⃣ Open the front‑end UI in the default browser
Start-Process -FilePath (Join-Path $PSScriptRoot "frontend\index.html")

Write-Host "✅ Liton Tea Store is up and running!" -ForegroundColor Green
