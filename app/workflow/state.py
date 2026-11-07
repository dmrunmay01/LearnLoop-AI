
from typing import TypedDict, Any


class WorkflowState(TypedDict, total=False):
    topic: str
    plan: dict
    reference_context: str
    source_ids: list[str]
    memory_context: str
    lesson: dict
    report: dict
    feedback: str
    attempt: int
    max_retries: int
    status: str
    rejection_log: list[dict]
    successful_strategies: list[str]
    run_id: int

    # Optional demonstration fault injection
    demo_error: str | None
    demo_error_injected: bool
