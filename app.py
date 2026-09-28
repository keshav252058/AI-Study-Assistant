import csv
from datetime import datetime
from pathlib import Path

import streamlit as st

from agent import (
    create_study_plan,
    ask_ai,
    generate_personalized_plan
)


# -----------------------------
# PAGE CONFIGURATION
# -----------------------------

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="centered"
)

st.title("📚 AI Study Assistant")
st.write(
    "Create study plans, track your progress, "
    "and get help from your local AI assistant."
)

st.divider()


# -----------------------------
# PROGRESS FILE
# -----------------------------

PROGRESS_FILE = Path(__file__).parent / "study_progress.csv"


def save_progress(subject, goal, tasks, completed_tasks):
    """Save study tasks and their status to a CSV file."""

    file_exists = PROGRESS_FILE.exists()

    with open(
        PROGRESS_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "date",
                "subject",
                "goal",
                "task",
                "status"
            ])

        saved_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for index, task in enumerate(tasks):
            status = (
                "Completed"
                if index in completed_tasks
                else "Pending"
            )

            writer.writerow([
                saved_at,
                subject,
                goal,
                task,
                status
            ])


def load_progress():
    """Read saved progress records from CSV."""

    if not PROGRESS_FILE.exists():
        return []

    with open(
        PROGRESS_FILE,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)
        return list(reader)


# -----------------------------
# STUDENT DETAILS
# -----------------------------

st.header("📝 Create Your Study Plan")

name = st.text_input(
    "Your name",
    placeholder="Enter your name"
)

subject = st.text_input(
    "Subject",
    placeholder="Example: Python"
)

goal = st.text_input(
    "Your study goal",
    placeholder="Example: Learn Python loops"
)

study_hours = st.number_input(
    "Study hours per day",
    min_value=1,
    max_value=12,
    value=2
)


# -----------------------------
# BASIC STUDY PLAN
# -----------------------------

if st.button("Generate Study Plan"):

    if not subject.strip() or not goal.strip():
        st.warning("Please enter your subject and study goal.")

    else:
        plan = create_study_plan(
            subject,
            goal,
            study_hours
        )

        st.session_state["study_plan"] = plan
        st.session_state["completed_tasks"] = []

        st.success(
            f"Study plan created for {name or 'Student'}!"
        )


# -----------------------------
# DISPLAY TASKS AND PROGRESS
# -----------------------------

if "study_plan" in st.session_state:

    plan = st.session_state["study_plan"]
    tasks = plan["tasks"]

    st.subheader(f"📌 Your {plan['subject']} Tasks")

    completed_tasks = st.session_state["completed_tasks"]

    for index, task in enumerate(tasks):

        checked = st.checkbox(
            task,
            value=index in completed_tasks,
            key=f"task_{index}"
        )

        if checked and index not in completed_tasks:
            completed_tasks.append(index)

        elif not checked and index in completed_tasks:
            completed_tasks.remove(index)

    progress = len(completed_tasks) / len(tasks)

    st.progress(progress)

    st.write(
        f"Progress: {len(completed_tasks)} of "
        f"{len(tasks)} tasks completed"
    )

    # Save progress button
    if st.button("💾 Save Study Progress"):

        save_progress(
            plan["subject"],
            plan["goal"],
            tasks,
            completed_tasks
        )

        st.success("Your study progress has been saved!")


st.divider()


# -----------------------------
# PERSONALIZED AI STUDY PLAN
# -----------------------------

st.header("🧠 Personalized AI Study Plan")

st.write(
    "Generate a study timetable based on your subject, "
    "goal, and available study hours."
)

if st.button("Create AI Study Plan"):

    if not subject.strip() or not goal.strip():

        st.warning("Please enter your subject and study goal above.")

    else:

        with st.spinner("AI is creating your personalized plan..."):

            try:
                ai_plan = generate_personalized_plan(
                    subject,
                    goal,
                    study_hours
                )

                st.session_state["ai_plan"] = ai_plan

            except Exception as error:
                st.error(
                    "Could not generate the AI study plan. "
                    "Please check that Ollama is running."
                )
                st.caption(str(error))


if "ai_plan" in st.session_state:

    st.subheader("Your AI-Generated Plan")
    st.markdown(st.session_state["ai_plan"])


st.divider()


# -----------------------------
# ASK AI
# -----------------------------

st.header("🤖 Ask Your AI Study Assistant")

question = st.text_area(
    "Enter your study question",
    placeholder="Example: Explain Python loops with an example."
)

if st.button("Ask AI"):

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        with st.spinner("AI is thinking..."):

            try:
                answer = ask_ai(question)

                st.session_state["last_question"] = question
                st.session_state["last_answer"] = answer

            except Exception as error:

                st.error(
                    "Could not connect to Ollama. "
                    "Please make sure Ollama is running."
                )

                st.caption(str(error))


if "last_answer" in st.session_state:

    st.subheader("AI Answer")
    st.markdown(st.session_state["last_answer"])


st.divider()


# -----------------------------
# SAVED STUDY HISTORY
# -----------------------------

st.header("📊 Saved Study History")

history = load_progress()

if history:

    st.write(f"Total saved task records: {len(history)}")

    st.dataframe(
        history,
        use_container_width=True,
        hide_index=True
    )

    csv_data = PROGRESS_FILE.read_bytes()

    st.download_button(
        label="⬇️ Download Study History CSV",
        data=csv_data,
        file_name="study_progress.csv",
        mime="text/csv"
    )

else:

    st.info(
        "No saved study history yet. "
        "Generate a study plan and click Save Study Progress."
    )


st.divider()

st.caption(
    "Powered by Python, Streamlit, and Ollama running locally."
)