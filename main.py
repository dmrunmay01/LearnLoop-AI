import argparse
import json
from pathlib import Path
from app.workflow.graph import run_lesson

def main():
    parser = argparse.ArgumentParser(description="LearnLoop AI: self-evaluating lesson generator")
    parser.add_argument("--topic", default="Introduction to RAG")
    parser.add_argument("--max-retries", type=int, default=2)
    parser.add_argument(
        "--demo-error",
        choices=["missing-glossary"],
        default=None,
        help="Intentionally remove the first draft's glossary to test self-correction."
    )

    args = parser.parse_args()

    result = run_lesson(
        topic=args.topic,
        max_retries=args.max_retries,
        demo_error=args.demo_error
    )
    Path("outputs").mkdir(exist_ok=True)
    output = {
        "topic": result.get("topic"),
        "status": result.get("status"),
        "attempt": result.get("attempt"),
        "run_id": result.get("run_id"),
        "lesson": result.get("lesson"),
        "evaluation": result.get("report"),
        "rejection_log": result.get("rejection_log", [])
    }
    out = Path("outputs/latest_run.json")
    out.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Status: {output['status']} | Run ID: {output['run_id']} | Retries: {output['attempt']}")
    print(f"Saved result to {out}")

if __name__ == "__main__":
    main()
