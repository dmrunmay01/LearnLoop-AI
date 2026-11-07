
import sys
from pathlib import Path

# Add project root to Python path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from app.workflow.graph import run_lesson

st.set_page_config(
    page_title="LearnLoop AI",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 LearnLoop AI")
st.caption("Agentic AI-powered lesson generation and evaluation")

# Sidebar
with st.sidebar:
    st.header("Generation Settings")
    topic = st.text_input("Lesson Topic", "Introduction to RAG")
    retries = st.slider("Maximum Retries", 0, 2, 2)

# Generate
if st.button("🚀 Generate Lesson", type="primary"):
    if not topic.strip():
        st.warning("Please enter a topic.")
    else:
        try:
            with st.spinner("Generating and evaluating lesson..."):
                st.session_state.result = run_lesson(
                    topic=topic,
                    max_retries=retries
                )
        except Exception as e:
            st.error(f"Error: {e}")

# Display results
if "result" in st.session_state:
    result = st.session_state.result
    lesson = result.get("lesson", {})
    report = result.get("report", {})
    checks = report.get("checks", [])

    passed = sum(c.get("passed", False) for c in checks)
    failed = len(checks) - passed

    st.divider()

    # Status
    if result.get("status") == "PUBLISHED":
        st.success("✅ Lesson Published")
    else:
        st.error("❌ Lesson Rejected")

    # Metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Evaluation", f"{passed}/{len(checks)}")
    c2.metric("Passed", passed)
    c3.metric("Failed", failed)
    c4.metric("Retries", result.get("attempt", 0))

    st.progress(passed / len(checks) if checks else 0)

    # Tabs
    lesson_tab, evaluation_tab, history_tab = st.tabs(
        ["📖 Lesson", "🔍 Evaluation", "🔄 Rejection History"]
    )

    with lesson_tab:
        st.header(lesson.get("title", "Generated Lesson"))
        st.markdown(lesson.get("introduction", ""))

        for section in lesson.get("sections", []):
            with st.expander(section.get("heading", "Section")):
                st.markdown(section.get("content", ""))

        st.subheader("Worked Example")
        st.markdown(lesson.get("worked_example", ""))

        st.subheader("Real-World Application")
        st.markdown(lesson.get("real_world_application", ""))

        st.subheader("Limitations")
        st.markdown(lesson.get("limitations", ""))

        st.subheader("Recap")
        for point in lesson.get("recap", []):
            st.markdown(f"- {point}")

        st.subheader("Glossary")
        for term, definition in lesson.get("glossary", {}).items():
            st.markdown(f"**{term}:** {definition}")

        st.subheader("Knowledge Check")
        for i, question in enumerate(lesson.get("knowledge_check", []), 1):
            with st.expander(f"Question {i}: {question['question']}"):
                st.write(f"Answer: {question['answer']}")

    with evaluation_tab:
        st.subheader("Quality Rubric")
        for check in checks:
            icon = "✅" if check.get("passed") else "❌"
            with st.expander(f"{icon} {check.get('check_id')}"):
                st.write(check.get("evidence", ""))
                if not check.get("passed"):
                    st.error(check.get("failure_reason", "Failed"))

    with history_tab:
        rejection_log = result.get("rejection_log", [])
        if rejection_log:
            for item in rejection_log:
                st.write(f"Attempt {item.get('attempt')}: REJECTED")
                st.write("Failed checks:", item.get("failed_checks", []))
                st.write("Reasons:", item.get("reasons", []))
        else:
            st.info("No rejection. The lesson passed its first attempt.")

    # Export
    st.divider()
    st.download_button(
        "📥 Download Run Results (JSON)",
        data=__import__("json").dumps(result, indent=2, ensure_ascii=False),
        file_name="learnloop_result.json",
        mime="application/json"
    )
