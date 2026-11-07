# Design decisions and trade-offs

| Decision | Rationale | Trade-off |
|---|---|---|
| LangGraph | Explicit state machine and conditional loops | Additional framework dependency |
| Separate evaluator | Reduces direct self-approval behavior | LLM evaluation remains imperfect |
| Hard pass/fail rubric | No critical weakness hidden by an average | Strict gate may reject useful drafts |
| SQLite memory | Durable, local, easy to inspect | Not intended for multi-instance production |
| Local reference corpus | Reproducible grounding for the assignment | Limited knowledge coverage |
| Deterministic + LLM checks | Structural reliability plus semantic judgment | Some checks still require model judgment |
| Two retries maximum | Bounded cost and guaranteed termination | Some lessons may remain rejected |
