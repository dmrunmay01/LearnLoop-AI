
from pydantic import BaseModel, Field


class LearningPlan(BaseModel):
    topic: str
    learner_profile: str = "Absolute beginner"
    learning_objectives: list[str] = Field(min_length=3, max_length=7)
    prerequisites: list[str]
    lesson_outline: list[str] = Field(min_length=5, max_length=10)
    key_terms: list[str]


class LessonSection(BaseModel):
    heading: str
    content: str


class KnowledgeQuestion(BaseModel):
    question: str
    answer: str


class Lesson(BaseModel):
    title: str
    introduction: str
    sections: list[LessonSection]
    worked_example: str
    real_world_application: str
    limitations: str
    recap: list[str]
    knowledge_check: list[KnowledgeQuestion]
    glossary: dict[str, str]
    source_notes: list[str] = Field(default_factory=list)


class RubricCheck(BaseModel):
    check_id: str
    dimension: str
    passed: bool
    evidence: str
    failure_reason: str = ""
    correction: str = ""


class EvaluationReport(BaseModel):
    checks: list[RubricCheck]
    overall_pass: bool
    summary: str
    critical_risks: list[str] = Field(default_factory=list)


class LessonRunState(dict):
    """Documentation marker for the LangGraph state shape."""
