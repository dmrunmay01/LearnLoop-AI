# LearnLoop AI

### Self-Evolving Agentic Lesson Engineering System

LearnLoop AI is an agentic educational content-generation system that creates beginner-friendly technical lessons, independently evaluates them against a strict quality rubric, regenerates rejected lessons using actionable feedback, and publishes only when every mandatory checkpoint passes.

## 1. Project Overview

LearnLoop AI demonstrates how agentic AI systems can improve generated educational content through structured planning, independent evaluation, bounded self-correction, and persistent cross-run memory.

Unlike a one-shot LLM application, LearnLoop implements a multi-stage workflow that can identify quality failures, explain why a lesson was rejected, regenerate content using corrective feedback, and publish only validated output.

**Assignment Topic:** Introduction to Retrieval-Augmented Generation (RAG)

**Target Learner:** A 12th-grade graduate in India with limited English vocabulary, no prior technical knowledge, and an interest in building a career in AI.

## 2. Core Capabilities

- Beginner-first curriculum planning and lesson generation.
- Multi-agent workflow orchestration using LangGraph.
- Independent evaluator with 12 binary quality checkpoints.
- Deterministic structural validation alongside LLM-based evaluation.
- Evidence, failure reasons, and correction instructions for failed checkpoints.
- Automatic regeneration using evaluator feedback.
- Maximum two regeneration attempts with a fail-closed publication gate.
- SQLite-based persistent memory for recurring failures and successful improvement strategies.
- Local reference retrieval for grounded technical explanations.
- Structured JSON output with Pydantic validation.
- Streamlit dashboard and FastAPI endpoint.
- Automated tests and documented engineering decisions.

## 3. System Architecture

The application follows a bounded agentic workflow:

1. **Planner Agent:** Creates a structured learning plan based on the topic and learner profile.
2. **Retrieval Component:** Retrieves relevant passages from the local reference corpus.
3. **Generator Agent:** Produces a structured, beginner-friendly lesson.
4. **Evaluator Agent:** Independently evaluates the lesson against all 12 mandatory quality checkpoints.
5. **Improvement Loop:** If evaluation fails, actionable feedback is passed to the generator for another attempt.
6. **Publication Gate:** Publishes the lesson only when every mandatory checkpoint passes.
7. **Memory System:** Stores recurring failures and successful correction strategies for future runs.

### Workflow

```text
              User Topic
                  |
                  v
             Planner Agent
                  |
                  v
           Reference Retrieval
                  |
                  v
            Generator Agent
                  |
                  v
           Generated Lesson
                  |
                  v
            Evaluator Agent
                  |
                  v
          12-Point Evaluation
                  |
             +----+----+
             |         |
          PASSED     FAILED
             |         |
             v         v
          Publish   Rejection Log
             |         |
             |         v
             |   Corrective Feedback
             |         |
             |         v
             |   Generator Retry
             |         |
             |         v
             |      Evaluate
             |         |
             +----<----+
                  |
                  v
           SQLite Memory
```

For detailed documentation, see:

- [Architecture](docs/architecture.md)
- [Evaluation Strategy](docs/evaluation_strategy.md)
- [Design Decisions](docs/design_decisions.md)

## 4. Model Experimentation and Engineering Decisions

During development, different LLM deployment approaches were explored to understand the trade-offs between local inference, hardware requirements, response latency, and hosted model availability.

### Initial Experiment: Microsoft Phi-3

- Initially experimented with Microsoft's Phi-3 model through Ollama.
- Explored local LLM inference without depending on a hosted inference API.
- Evaluated generation performance under consumer hardware constraints.
- Experienced slower generation during development, particularly for lengthy structured lessons.

### Transition to Groq

To improve development speed and generation responsiveness, the implementation was switched to Groq-hosted inference using `openai/gpt-oss-20b`.

This provided a more practical environment for iterative generation, evaluation, and regeneration experiments.

### Configurable Model Provider

The LLM integration was designed to support multiple providers:

| Provider | Model / Configuration | Purpose |
|---|---|---|
| Ollama | Phi-3 | Initial local inference experimentation |
| Groq | openai/gpt-oss-20b | Current working generation configuration |
| OpenAI | gpt-4o-mini | Alternative supported provider |

The provider can be configured through environment variables without changing the agent workflow.

## 5. Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python 3.11 |
| Agent Orchestration | LangGraph |
| LLM Integration | LangChain |
| Current LLM Provider | Groq |
| Initial Local Model Experiment | Microsoft Phi-3 via Ollama |
| Alternative LLM Providers | OpenAI, Ollama |
| Structured Output Validation | Pydantic |
| Persistent Memory | SQLite |
| Reference Retrieval | Custom lexical retriever |
| Dashboard | Streamlit |
| API | FastAPI |
| Testing | Pytest |

## 6. Project Structure

```text
LearnLoop-AI/
|
|-- app/
|   |-- agents/
|   |   |-- planner.py
|   |   |-- generator.py
|   |   |-- evaluator.py
|   |   |-- llm.py
|   |
|   |-- evaluation/
|   |   |-- rubric.py
|   |   |-- validators.py
|   |
|   |-- workflow/
|   |   |-- graph.py
|   |   |-- state.py
|   |
|   |-- memory/
|   |   |-- database.py
|   |
|   |-- retrieval/
|   |   |-- retriever.py
|   |
|   |-- config.py
|   |-- schemas.py
|
|-- dashboard/
|   |-- app.py
|
|-- data/
|   |-- reference_material/
|
|-- docs/
|   |-- architecture.md
|   |-- evaluation_strategy.md
|   |-- design_decisions.md
|
|-- outputs/
|   |-- latest_run.json
|
|-- tests/
|
|-- api.py
|-- main.py
|-- requirements.txt
|-- .env.example
|-- .gitignore
|-- README.md
```

## 7. Installation and Setup

### Prerequisites

- Python 3.11 or later.
- Git.
- A Groq API key for the recommended configuration.

### Step 1: Clone the repository

```bash
git clone https://github.com/dmrunmay01/LearnLoop-AI.git
cd LearnLoop-AI
```

### Step 2: Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment:

**Windows PowerShell**

```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux**

```bash
source .venv/bin/activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure environment variables

Copy the example environment file:

**Windows PowerShell**

```powershell
Copy-Item .env.example .env
```

Configure your preferred provider in `.env`.

**Groq (recommended configuration)**

```env
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-20b
```

**OpenAI**

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini
```

**Ollama**

```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=phi3:latest
OLLAMA_BASE_URL=http://localhost:11434
```

For Ollama, install and start Ollama, then pull the selected model.

Never commit your `.env` file or expose API keys.

## 8. Running the Application

### Generate a lesson

```bash
python main.py --topic "Introduction to RAG" --max-retries 2
```

The workflow generates, evaluates, and publishes the lesson if all mandatory checkpoints pass.

The latest result is saved to:

```text
outputs/latest_run.json
```

### Demonstrate self-correction

LearnLoop includes an optional demonstration fault injection that deliberately removes the glossary from the first generated draft.

Run:

```bash
python main.py --topic "Introduction to RAG" --max-retries 1 --demo-error missing-glossary
```

Expected workflow:

1. The first lesson is generated with a missing glossary.
2. The evaluator identifies the failure under checkpoint JAR-02.
3. The lesson is rejected and the reason is recorded.
4. Corrective feedback is passed to the generator.
5. The generator produces a revised lesson.
6. The evaluator checks the revised lesson.
7. The lesson is published if all 12 checkpoints pass.

This feature demonstrates the system's self-correction capability and is intended for testing and demonstration.

### Launch the Streamlit dashboard

```bash
streamlit run dashboard/app.py
```

### Launch the FastAPI server

```bash
uvicorn api:app --reload
```

Available endpoints:

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Application health check |
| POST | `/generate` | Generate and evaluate a lesson |
| GET | `/runs` | Retrieve previous runs |

Example API request:

```json
{
  "topic": "Introduction to RAG",
  "max_retries": 2
}
```

### Run automated tests

```bash
pytest -q
```

## 9. Evaluation Framework

LearnLoop uses a strict 12-checkpoint evaluation rubric.

Each checkpoint is binary: PASS or FAIL. Partial credit is not permitted.

The evaluator assesses:

- Accuracy and factual reliability.
- Beginner accessibility and clarity.
- Completeness of examples and explanations.
- Glossary quality and technical coverage.
- Logical lesson flow and learning structure.

Deterministic validators independently enforce important structural requirements, while the LLM evaluator assesses semantic quality.

A lesson is published only when every mandatory checkpoint passes.

If evaluation fails, the system can regenerate the lesson up to the configured retry limit. If the retry limit is exhausted, the lesson is rejected.

## 10. Persistent Memory and Cross-Run Learning

LearnLoop uses SQLite to maintain persistent memory across separate executions.

The memory system stores:

- Previous run status, lesson, evaluation report, and attempt count.
- Recurring failed rubric checkpoint IDs.
- Failure occurrence counts and latest failure reasons.
- Correction strategies that have previously resulted in successful improvements.

During subsequent runs, the memory system retrieves relevant information and provides it to the generator as advisory context.

Memory does not modify the evaluation rubric or override the publication gate.

This allows the system to learn from recurring quality issues while preserving consistent evaluation standards.

## 11. Grounding and Reference Retrieval

The starter reference corpus is located in:

```text
data/reference_material/
```

A custom lexical retriever searches the local reference material and supplies relevant passages to the planning, generation, and evaluation stages.

Additional curated Markdown documents can be added to expand the reference corpus.

The retrieval component helps ground lesson content in supplied reference material rather than relying entirely on model-generated knowledge.

## 12. Important Limitations

- LLM-based evaluation is not proof of factual correctness.
- Semantic evaluation can produce incorrect judgments.
- Retrieval may return incomplete or irrelevant passages.
- Persistent memory provides advisory context and does not guarantee better output.
- The system requires human review for high-stakes educational content.
- Generation quality and response latency depend on the selected model and provider.

The system is designed as an applied AI engineering demonstration rather than a production-ready educational publishing platform.

## 13. Demonstration Checklist

A complete demonstration can follow this sequence:

1. Launch the LearnLoop dashboard.
2. Generate an Introduction to RAG lesson.
3. Show the generated lesson and evaluation results.
4. Demonstrate the deliberate missing-glossary failure.
5. Show the evaluator rejecting the first draft.
6. Show corrective feedback and automatic regeneration.
7. Demonstrate the final passing lesson.
8. Inspect the rejection log.
9. Show SQLite persistent memory and cross-run retrieval.
10. Execute the automated test suite.

## 14. Current Validation Results

The development workflow has been tested with a deliberate glossary failure.

| Validation | Result |
|---|---|
| Initial draft | Rejected |
| Failure identified | JAR-02 |
| Regeneration attempts | 1 |
| Final publication status | PUBLISHED |
| Final evaluation | 12/12 passed |
| Glossary terms in final lesson | 5 |
| Persistent failure memory | Verified |
| Successful improvement memory | Verified |
| Memory retrieval | Verified |
| Automated tests | 8 passed, 0 failed |

These results demonstrate the working self-correction and persistent-memory workflow.

---

**LearnLoop AI**

*Reliable AI-generated educational content requires structured planning, measurable quality gates, bounded self-correction, persistent learning, and transparent publication decisions.*