
from langgraph.graph import StateGraph, END

from app.workflow.state import WorkflowState
from app.agents.planner import create_plan
from app.agents.generator import generate_lesson
from app.agents.evaluator import evaluate_lesson, format_feedback
from app.memory.database import MemoryStore
from app.retrieval.retriever import retrieve
from app.config import settings


def build_graph(memory: MemoryStore | None = None):
    store = memory or MemoryStore(settings.database_path)

    def plan_node(state: WorkflowState):
        chunks = retrieve(state["topic"], top_k=6)
        context = "\n\n".join(f"[{c.source}] {c.text}" for c in chunks)
        plan = create_plan(state["topic"], context)

        return {
            "plan": plan,
            "reference_context": context or
            "No local reference material found. Use cautious, established knowledge and flag uncertainty.",
            "source_ids": [c.source for c in chunks],
            "memory_context": store.get_memory_context()
        }

    def generate_node(state: WorkflowState):
        lesson = generate_lesson(
            state["topic"],
            state["plan"],
            state["reference_context"],
            state.get("feedback", ""),
            state.get("memory_context", "")
        )

        # Optional deliberate error for self-correction testing
        inject_error = (
            state.get("demo_error") == "missing-glossary"
            and state.get("attempt", 0) == 0
            and not state.get("demo_error_injected", False)
        )

        if inject_error:
            lesson["glossary"] = {}
            return {
                "lesson": lesson,
                "demo_error_injected": True
            }

        return {"lesson": lesson}

    def evaluate_node(state: WorkflowState):
        report = evaluate_lesson(
            state["lesson"],
            state["reference_context"]
        )
        return {"report": report}

    def route_after_evaluation(state: WorkflowState):
        if state["report"]["overall_pass"]:
            return "publish"

        if state.get("attempt", 0) >= state.get(
            "max_retries", settings.max_retries
        ):
            return "reject"

        return "improve"

    def improve_node(state: WorkflowState):
        report = state["report"]

        store.record_failures(report["checks"])

        failed = [
            c for c in report["checks"] if not c["passed"]
        ]

        strategies = [
            c.get("correction", "")
            for c in failed if c.get("correction")
        ]

        feedback = format_feedback(report)

        rejection = {
            "attempt": state.get("attempt", 0) + 1,
            "status": "REJECTED",
            "failed_checks": [c["check_id"] for c in failed],
            "reasons": [
                c.get("failure_reason", "") for c in failed
            ],
            "changes_requested": strategies
        }

        return {
            "attempt": state.get("attempt", 0) + 1,
            "feedback": feedback,
            "rejection_log": (
                state.get("rejection_log", []) + [rejection]
            ),
            "successful_strategies": (
                state.get("successful_strategies", []) + strategies
            )
        }

    def publish_node(state: WorkflowState):
        store.record_improvements(
            state.get("successful_strategies", [])
        )

        run_id = store.save_run(
            state["topic"],
            "PUBLISHED",
            state.get("attempt", 0),
            state["lesson"],
            state["report"]
        )

        return {"status": "PUBLISHED", "run_id": run_id}

    def reject_node(state: WorkflowState):
        store.record_failures(state["report"]["checks"])

        run_id = store.save_run(
            state["topic"],
            "REJECTED",
            state.get("attempt", 0),
            state["lesson"],
            state["report"]
        )

        return {"status": "REJECTED", "run_id": run_id}

    # Build and compile the LangGraph workflow
    graph = StateGraph(WorkflowState)

    graph.add_node("plan", plan_node)
    graph.add_node("generate", generate_node)
    graph.add_node("evaluate", evaluate_node)
    graph.add_node("improve", improve_node)
    graph.add_node("publish", publish_node)
    graph.add_node("reject", reject_node)

    graph.set_entry_point("plan")

    graph.add_edge("plan", "generate")
    graph.add_edge("generate", "evaluate")

    graph.add_conditional_edges(
        "evaluate",
        route_after_evaluation,
        {
            "publish": "publish",
            "improve": "improve",
            "reject": "reject"
        }
    )

    graph.add_edge("improve", "generate")
    graph.add_edge("publish", END)
    graph.add_edge("reject", END)

    return graph.compile()


def run_lesson(
    topic: str,
    max_retries: int | None = None,
    demo_error: str | None = None
):
    store = MemoryStore(settings.database_path)
    graph = build_graph(store)

    return graph.invoke({
        "topic": topic,
        "attempt": 0,
        "max_retries": (
            settings.max_retries
            if max_retries is None
            else min(max(max_retries, 0), 2)
        ),
        "rejection_log": [],
        "successful_strategies": [],
        "status": "RUNNING",
        "demo_error": demo_error,
        "demo_error_injected": False
    })
