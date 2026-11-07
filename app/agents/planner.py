from app.agents.llm import get_chat_model
from app.schemas import LearningPlan

def create_plan(topic: str, reference_context: str) -> dict:
    model = get_chat_model(0.1).with_structured_output(
    LearningPlan,
    method="json_schema"
)
    prompt = f"""You are a learning experience designer. Design a beginner lesson plan.
Assume the learner starts from absolute zero. Avoid assumed prerequisites.
Topic: {topic}
Reference context:
{reference_context}
Return 3-7 measurable objectives, a logical 5-10 section outline, key terms and prerequisites.
Do not teach the lesson yet. Do not invent facts beyond standard well-established knowledge and reference context."""
    return model.invoke(prompt).model_dump()
