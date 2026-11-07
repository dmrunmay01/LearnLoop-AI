from app.evaluation.rubric import RUBRIC
from app.evaluation.validators import deterministic_checks

def valid_lesson():
    return {
        "sections": [{"heading": "Chunking", "content": "A chunk is a small piece. Embeddings represent meaning. Retrieval finds relevant chunks."} for _ in range(4)],
        "worked_example": "A learner asks a question. The system retrieves relevant chunks from a document, adds them as context to the language model, and the model generates an answer grounded in that context. " * 2,
        "real_world_application": "A college helpdesk can retrieve current policy documents before answering student questions. " * 2,
        "glossary": {"RAG":"", "chunk":"", "embedding":"", "retrieval":""},
        "recap": ["a","b","c"],
        "knowledge_check": [{"question":"q","answer":"a"} for _ in range(3)]
    }

def test_rubric_has_twelve_mandatory_checks():
    assert len(RUBRIC) == 12
    assert len({r["check_id"] for r in RUBRIC}) == 12

def test_deterministic_checks_pass_complete_structure():
    results = deterministic_checks(valid_lesson())
    assert all(r["passed"] for r in results)

def test_deterministic_checks_fail_missing_example():
    lesson = valid_lesson()
    lesson["worked_example"] = "Too short."
    results = {r["check_id"]: r for r in deterministic_checks(lesson)}
    assert results["EX-01"]["passed"] is False
