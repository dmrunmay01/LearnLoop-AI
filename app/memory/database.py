import sqlite3
from pathlib import Path
import json
from datetime import datetime, timezone

class MemoryStore:
    def __init__(self, db_path: str = "data/learnloop.db"):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _initialize(self):
        with self._connect() as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS runs (
                run_id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT, status TEXT, attempts INTEGER,
                lesson_json TEXT, report_json TEXT, created_at TEXT
            )""")
            conn.execute("""CREATE TABLE IF NOT EXISTS failure_patterns (
                pattern TEXT PRIMARY KEY, occurrences INTEGER DEFAULT 0,
                latest_reason TEXT, updated_at TEXT
            )""")
            conn.execute("""CREATE TABLE IF NOT EXISTS improvements (
                strategy TEXT PRIMARY KEY, successes INTEGER DEFAULT 0,
                updated_at TEXT
            )""")

    def save_run(self, topic, status, attempts, lesson, report):
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO runs(topic,status,attempts,lesson_json,report_json,created_at) VALUES(?,?,?,?,?,?)",
                (topic, status, attempts, json.dumps(lesson), json.dumps(report),
                 datetime.now(timezone.utc).isoformat())
            )
            return cur.lastrowid

    def record_failures(self, checks):
        now = datetime.now(timezone.utc).isoformat()
        with self._connect() as conn:
            for check in checks:
                if not check.get("passed"):
                    key = check.get("check_id", "UNKNOWN")
                    reason = check.get("failure_reason", "")
                    conn.execute("""INSERT INTO failure_patterns(pattern,occurrences,latest_reason,updated_at)
                        VALUES(?,1,?,?) ON CONFLICT(pattern) DO UPDATE SET
                        occurrences=occurrences+1, latest_reason=excluded.latest_reason, updated_at=excluded.updated_at""",
                        (key, reason, now))

    def record_improvements(self, strategies):
        now = datetime.now(timezone.utc).isoformat()
        with self._connect() as conn:
            for strategy in strategies:
                if strategy.strip():
                    conn.execute("""INSERT INTO improvements(strategy,successes,updated_at)
                        VALUES(?,1,?) ON CONFLICT(strategy) DO UPDATE SET
                        successes=successes+1, updated_at=excluded.updated_at""",
                        (strategy.strip(), now))

    def get_memory_context(self, limit=8):
        with self._connect() as conn:
            failures = conn.execute(
                "SELECT pattern, occurrences, latest_reason FROM failure_patterns ORDER BY occurrences DESC LIMIT ?", (limit,)
            ).fetchall()
            improvements = conn.execute(
                "SELECT strategy, successes FROM improvements ORDER BY successes DESC LIMIT ?", (limit,)
            ).fetchall()
        lines = ["Cross-run learning memory (advisory; never changes the rubric):"]
        lines += [f"- Recurring failure {p}: {n} occurrence(s). Latest reason: {r}" for p,n,r in failures]
        lines += [f"- Previously useful correction ({n} success records): {s}" for s,n in improvements]
        return "\n".join(lines)

    def recent_runs(self, limit=20):
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT run_id,topic,status,attempts,created_at FROM runs ORDER BY run_id DESC LIMIT ?", (limit,)
            ).fetchall()
        return rows
