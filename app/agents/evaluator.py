from app.agents.llm import get_chat_model
from app.schemas import EvaluationReport
from app.evaluation.rubric import RUBRIC
from app.evaluation.validators import deterministic_checks

def evaluate_lesson(lesson: dict, reference_context: str) -> dict:
    model = get_chat_model(0).with_structured_output(
    EvaluationReport,
    method="json_schema"
)
    rubric_text = "\n".join(f"{r['check_id']} | {r['dimension']} | {r['criterion']}" for r in RUBRIC)
    prompt = f"""You are an independent, skeptical educational quality auditor.
Evaluate the lesson against EVERY rubric checkpoint. A check passes only if the lesson
contains clear evidence that fully satisfies the criterion. No partial credit.
Do not reward intentions or infer content that is not present. Cite concise evidence.
For factual checks, compare claims to the trusted reference context and established RAG
principles. If uncertain or unsupported, fail and explain the risk.
Rubric:
{rubric_text}
Trusted reference context:
{reference_context}
Lesson:
{lesson}
Return exactly one result for every check ID. overall_pass is true only if every check passes.
For failed checks provide a specific correction that a generator can act on."""
    llm_report = model.invoke(prompt).model_dump()
    deterministic = {c["check_id"]: c for c in deterministic_checks(lesson)}
    merged = []
    for check in llm_report.get("checks", []):
        hard = deterministic.get(check["check_id"])
        if hard and not hard["passed"]:
            check["passed"] = False
            check["failure_reason"] = hard["failure_reason"]
            check["correction"] = hard["correction"]
            check["evidence"] = hard["evidence"]
        merged.append(check)
    expected = {r["check_id"] for r in RUBRIC}
    seen = {c["check_id"] for c in merged}
    for missing in sorted(expected - seen):
        r = next(x for x in RUBRIC if x["check_id"] == missing)
        merged.append({
            "check_id": missing, "dimension": r["dimension"], "passed": False,
            "evidence": "Evaluator omitted this mandatory checkpoint.",
            "failure_reason": "Missing evaluator result; fail-closed policy applied.",
            "correction": "Re-evaluate and explicitly satisfy this checkpoint."
        })
    for check in merged:
        hard = deterministic.get(check["check_id"])
        if hard and not hard["passed"]:
            check["passed"] = False
    overall = len(merged) == len(expected) and all(c["passed"] for c in merged)
    return {
        "checks": merged,
        "overall_pass": overall,
        "summary": llm_report.get("summary", "Evaluation completed."),
        "critical_risks": llm_report.get("critical_risks", [])
    }

def format_feedback(report: dict) -> str:
    failed = [c for c in report["checks"] if not c["passed"]]
    if not failed:
        return "No failed checkpoints."
    return "\n".join(
        f"- {c['check_id']} ({c['dimension']}): {c.get('failure_reason','')} "
        f"Required correction: {c.get('correction','')} Evidence: {c.get('evidence','')}"
        for c in failed
    )
