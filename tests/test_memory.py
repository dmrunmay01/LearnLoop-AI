from app.memory.database import MemoryStore

def test_memory_persists_failure_and_improvement(tmp_path):
    store = MemoryStore(str(tmp_path / "memory.db"))
    store.record_failures([{"check_id":"JAR-01","passed":False,"failure_reason":"Unexplained jargon"}])
    store.record_improvements(["Define jargon before first use"])
    context = store.get_memory_context()
    assert "JAR-01" in context
    assert "Define jargon before first use" in context

def test_run_history(tmp_path):
    store = MemoryStore(str(tmp_path / "memory.db"))
    run_id = store.save_run("Introduction to RAG", "REJECTED", 2, {}, {})
    assert run_id == 1
    assert store.recent_runs()[0][2] == "REJECTED"
