# Evaluation strategy

The release gate has 12 mandatory binary checks across accuracy/grounding, beginner friendliness, examples, jargon clarity, coverage, and teaching flow.

A check passes only when the evaluator identifies direct evidence. Missing evaluator results fail closed. Structural checks independently enforce the worked example, practical application, glossary, coverage structure, recap, and knowledge-check minimums.

No weighted average is used: all checks must pass. A failed lesson is regenerated using explicit failed check IDs, reasons, evidence, and correction instructions. At most two retries are allowed. If the final attempt fails, the run is marked REJECTED and is never described as published.

Memory records repeated failure categories and correction strategies. Memory informs future generation but cannot alter the rubric or turn a failed check into a pass.
