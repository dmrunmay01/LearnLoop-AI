
import re
from app.evaluation.rubric import RUBRIC


def normalize_items(value):
    """Convert strings and lists into separate non-empty items."""
    if isinstance(value, str):
        items = [value]
    elif isinstance(value, list):
        items = value
    else:
        items = []

    normalized = []

    for item in items:
        if isinstance(item, str):
            parts = re.split(r"\n+", item)
            normalized.extend(
                part.strip() for part in parts if part.strip()
            )
        elif item:
            normalized.append(str(item).strip())

    return normalized


def deterministic_checks(lesson: dict) -> list[dict]:
    """Hard structural checks that cannot be overridden by the LLM."""

    sections = lesson.get("sections", []) or []
    questions = lesson.get("knowledge_check", []) or []
    glossary = lesson.get("glossary", {}) or {}
    recap = normalize_items(lesson.get("recap", []))

    text = " ".join([
        str(lesson.get("introduction", "")),
        " ".join(
            str(s.get("heading", "")) + " " +
            str(s.get("content", ""))
            for s in sections
        ),
        str(lesson.get("worked_example", "")),
        str(lesson.get("real_world_application", "")),
        str(lesson.get("limitations", "")),
        " ".join(recap),
    ]).lower()

    checks = {
        "EX-01": len(str(lesson.get("worked_example", ""))) >= 120,
        "EX-02": len(str(lesson.get("real_world_application", ""))) >= 60,
        "JAR-02": len(glossary) >= 4,
        "COV-02": (
            all(term in text for term in ["chunk", "embedding", "retriev"])
            and len(sections) >= 4
        ),
        "FLOW-02": len(recap) >= 3 and len(questions) >= 3,
    }

    return [
        {
            "check_id": item["check_id"],
            "dimension": item["dimension"],
            "passed": checks[item["check_id"]],
            "evidence": (
                f"Deterministic validation: {len(recap)} recap points, "
                f"{len(questions)} knowledge questions."
            ),
            "failure_reason": (
                "" if checks[item["check_id"]]
                else "Required lesson structure or minimum content was not found."
            ),
            "correction": (
                "" if checks[item["check_id"]]
                else "Add the missing required content and meet the minimum structural requirement."
            ),
        }
        for item in RUBRIC
        if item["check_id"] in checks
    ]
