# LearnLoop AI — Architecture

## Objective
Generate a standalone beginner lesson, independently evaluate it against hard pass/fail checks, regenerate rejected content at most twice, and publish only when every mandatory check passes.

## Workflow
1. **Plan:** retrieve local reference passages and create measurable objectives and a teaching outline.
2. **Generate:** create a structured lesson using the plan, references, rubric, cross-run memory, and prior rejection feedback.
3. **Evaluate:** an independent evaluator returns a result for every rubric checkpoint. Deterministic structural validators independently enforce minimum content requirements.
4. **Route:** publish on unanimous pass; otherwise regenerate while attempts remain; reject after the retry limit.
5. **Persist:** save run artifacts, recurring failure patterns, and correction strategies in SQLite.

## Design decisions
- LangGraph provides explicit state and conditional routing.
- Pydantic enforces structured model output.
- Generator and evaluator have separate roles and prompts.
- The evaluator fails closed when it omits a required check.
- Deterministic validators complement model-based semantic evaluation.
- SQLite provides simple persistent memory without external infrastructure.
- Local Markdown reference material provides a transparent grounding corpus.
- The retry limit is clamped to 0–2 to guarantee termination.

## Limitations
The evaluator is still an LLM judge for semantic and factual quality. Deterministic checks validate structure, not truth. The local lexical retriever is intentionally lightweight; production deployment should use a stronger retriever, curated sources, claim-level verification, human review for high-stakes content, and calibrated evaluation datasets.
