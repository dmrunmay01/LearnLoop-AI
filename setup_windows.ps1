$ErrorActionPreference = "Stop"
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
if (!(Test-Path .env)) { Copy-Item .env.example .env }
Write-Host "Environment ready. Edit .env, then run: python main.py --topic 'Introduction to RAG'"
