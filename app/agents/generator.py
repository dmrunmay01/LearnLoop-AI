
import json
import re

from app.agents.llm import get_chat_model
from app.schemas import Lesson
from app.evaluation.rubric import RUBRIC


def generate_lesson(
    topic: str,
    plan: dict,
    reference_context: str,
    feedback: str = "",
    memory_context: str = ""
) -> dict:

    model = get_chat_model(0.2).with_structured_output(
    Lesson,
    method="json_mode"
)

    rubric_text = "\n".join(
        f"{r['check_id']}: {r['criterion']}"
        for r in RUBRIC
    )

    prompt = f"""
You are an expert technical educator creating a complete,
standalone lesson for an absolute beginner.

Return ONLY a valid JSON object. Do not use Markdown fences.
The JSON must match this exact structure:

{{
  "title": "string",
  "introduction": "string",
  "sections": [
    {{"heading": "string", "content": "string"}}
  ],
  "worked_example": "string",
  "real_world_application": "string",
  "limitations": "string",
  "recap": ["string"],
  "knowledge_check": [
    {{"question": "string", "answer": "string"}}
  ],
  "glossary": {{"term": "definition"}},
  "source_notes": ["string"]
}}

TOPIC:
{topic}

LEARNER:
Absolute beginner. Assume no prior technical knowledge.
The learner is a 12th-grade graduate in India with limited
English vocabulary and wants to build a career in AI.

LEARNING PLAN:
{json.dumps(plan, ensure_ascii=False)}

TRUSTED REFERENCE MATERIAL:
{reference_context}

MANDATORY QUALITY RUBRIC:
{rubric_text}

PREVIOUS EVALUATION FEEDBACK:
{feedback or "First generation attempt. No previous feedback."}

CROSS-RUN MEMORY:
{memory_context}

CONTENT REQUIREMENTS:
1. Create 5 logically ordered sections covering:
   - What RAG is and why it matters.
   - Embeddings and chunking.
   - Retrieval and vector search.
   - Context injection.
   - Answer generation and workflow.
2. Include a detailed worked example with a question,
   retrieved information, supplied context and final answer.
3. Explain a practical real-world application.
4. Explain retrieval errors, outdated information,
   missing context and possible hallucinations.
5. Include at least 4 recap points.
6. Include at least 3 questions, each with its own answer.
7. Define at least 5 technical terms in the glossary.
8. Use only supplied source identifiers in source_notes.
9. Explain technical terms in simple English.
10. Never claim RAG guarantees correctness.
11. Do not invent factual claims.

Return a complete JSON object with every required field.
"""

    result = model.invoke(prompt)
    return result.model_dump()