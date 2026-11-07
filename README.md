# LearnLoop AI 🎓
### Self-Evolving Agentic Lesson Engineering System

LearnLoop AI generates beginner-friendly technical lessons, independently evaluates them against a strict quality rubric, regenerates rejected lessons using actionable feedback, and publishes only when every mandatory checkpoint passes.

## Why this project?
This is not a one-shot prompt wrapper. It is a bounded agentic workflow with planning, generation, independent evaluation, conditional regeneration, persistent memory, and an auditable release decision.

## Core capabilities
- Beginner-first curriculum planning and lesson generation
- Independent evaluator with 12 binary quality checkpoints
- Deterministic structural validators alongside LLM evaluation
- Evidence, failure reasons, and correction instructions per failed check
- Maximum two regeneration attempts; fail-closed publication gate
- SQLite run history, recurring failure memory, and improvement strategies
- Local reference retrieval for grounded RAG explanations
- Streamlit dashboard and FastAPI endpoint
- Automated tests and documented design trade-offs

## Architecture
See [architecture](docs/architecture.md), [evaluation strategy](docs/evaluation_strategy.md), and [design decisions](docs/design_decisions.md).

## Quick start

### 1. Create environment
```bash
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure model
```bash
copy .env.example .env
```
Edit `.env` and choose one provider.

**OpenAI**
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key
OPENAI_MODEL=gpt-4o-mini
```

**Ollama**
```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.1
OLLAMA_BASE_URL=http://localhost:11434
```
For Ollama, install and start Ollama, then pull the selected model.

### 4. Run the assignment topic
```bash
python main.py --topic "Introduction to RAG" --max-retries 2
```
The full output is saved to `outputs/latest_run.json`.

### 5. Launch dashboard
```bash
streamlit run dashboard/app.py
```

### 6. Launch API
```bash
uvicorn api:app --reload
```
- `GET /health`
- `POST /generate` with `{"topic":"Introduction to RAG","max_retries":2}`
- `GET /runs`

### 7. Run tests
```bash
pytest -q
```

## Evaluation rubric
All 12 checks must pass. There is no averaging or partial credit. If any mandatory check fails, the generator receives structured feedback and can retry up to two times. After the limit, the lesson is rejected, not published.

## Memory
SQLite persists:
- run status, lesson, report, and attempt count
- recurring failed rubric IDs and latest reasons
- correction strategies that were used successfully

Memory is advisory. It cannot modify the rubric or override the quality gate.

## Grounding
The starter corpus is in `data/reference_material/`. A transparent lexical retriever supplies relevant passages to planning, generation, and evaluation. Add curated sources as Markdown files to expand the corpus.

## Important limitations
LLM-as-judge is not a proof of factual correctness. Structural checks are deterministic, but semantic evaluation can be wrong. The system documents this limitation and is designed to support human review and stronger verification in a production deployment.

## Suggested demo
1. Run `Introduction to RAG`.
2. Show each rubric result and evidence.
3. If rejected, show the rejection log and corrected retry.
4. Run a second topic to demonstrate cross-run memory.
5. Show SQLite-backed run history and test results.

## Tech stack
Python • LangGraph • LangChain • Pydantic • SQLite • FastAPI • Streamlit • Pytest

---
Built as an applied AI engineering demonstration: reliable generation requires measurable quality gates, bounded retries, persistent learning, and transparent decisions.
