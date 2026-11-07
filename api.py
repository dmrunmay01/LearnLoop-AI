from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from app.workflow.graph import run_lesson
from app.memory.database import MemoryStore
from app.config import settings

app = FastAPI(title="LearnLoop AI", version="1.0.0",
              description="Self-evaluating agentic lesson content generation system")

class GenerateRequest(BaseModel):
    topic: str = Field(min_length=2, max_length=200)
    max_retries: int = Field(default=2, ge=0, le=2)

@app.get("/health")
def health():
    return {"status": "ok", "service": "LearnLoop AI"}

@app.post("/generate")
def generate(request: GenerateRequest):
    try:
        result = run_lesson(request.topic, request.max_retries)
        return {
            "status": result.get("status"),
            "run_id": result.get("run_id"),
            "attempt": result.get("attempt"),
            "lesson": result.get("lesson"),
            "evaluation": result.get("report"),
            "rejection_log": result.get("rejection_log", [])
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@app.get("/runs")
def runs():
    return {"runs": MemoryStore(settings.database_path).recent_runs()}
