import streamlit as st
st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="centered"
)
import csv
from datetime import datetime
st.markdown("""
<style>
.stApp {
    background-color: #f5f7fb;
    color: #1f2937;
}

h1, h2, h3, p, label, .stMarkdown {
    color: #1f2937 !important;
}

.stTextInput label,
.stNumberInput label {
    color: #1f2937 !important;
}

.stTextInput input,
.stNumberInput input {
    background-color: white !important;
    color: #1f2937 !important;
}

.stButton > button {
    background-color: #2563eb;
    color: white !important;
    border-radius: 8px;
    border: none;
    padding: 10px 20px;
}

.stButton > button:hover {
    background-color: #1d4ed8;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)
st.title("AI Study Assistant")
st.write("Your personal study planner")

name = st.text_input("Enter your name")
subject = st.text_input("Which subject do you want to study?")
goal = st.text_input("What is your study goal?")

study_time = st.number_input(
    "How many hours can you study today?",
    min_value=1,
    max_value=12,
    value=2
)

if "show_plan" not in st.session_state:
    st.session_state.show_plan = False

if st.button("Generate Study Plan"):
    st.session_state.show_plan = True

if st.session_state.show_plan:
    if name and subject and goal:
        st.success(f"Hello {name}! Here is your study plan:")

        st.write(f"**Subject:** {subject}")
        st.write(f"**Goal:** {goal}")
        st.write(f"**Available time:** {study_time} hours")
        if subject.lower() == "python":
                st.info("Tip: Learn one concept, write a small program, and practice it.")
        elif subject.lower() == "java":
            st.info("Tip: Revise OOP concepts and practice small Java programs.")
        elif subject.lower() in ["ds", "data structures"]:
            st.info("Tip: Understand one data structure and solve a few practice questions.")
        else:
            st.info("Tip: Break your topic into small parts, revise, and practice questions.")
        if study_time <= 1:
         st.info("Focus on one important topic today.")
        elif study_time <= 3:
            st.info("Study one topic and practice questions.")
        else:
            st.info("Divide your time between learning, revision, and practice.")
            st.subheader("Your Daily Timetable")

        for hour in range(1, study_time + 1):
            if hour == 1:
                activity = "Learn a new topic"
            elif hour == 2:
                activity = "Practice questions"
            elif hour == 3:
                activity = "Revise what you learned"
            else:
                activity = "Solve questions and review mistakes"

            st.write(f"Hour {hour}: {activity}")
        tasks = [
            "Revise the basics of " + subject,
            "Work on your goal: " + goal,
            "Practice questions related to " + subject,
            "Review what you learned today"
        ]
        if st.button("Reset Plan"):
            st.session_state.show_plan = False
            st.rerun()
        st.subheader("Your Tasks")

        completed = 0

        for i, task in enumerate(tasks):
            if st.checkbox(task, key=f"task_{i}"):
                completed += 1

        progress = completed / len(tasks)

        st.progress(progress)
        st.write(f"Completed: {completed} / {len(tasks)} tasks")
    try:
        with open("study_progress.csv", "rb") as file:
                csv_data = file.read()

        st.download_button(
                label="Download My Progress CSV",
                data=csv_data,
                file_name="study_progress.csv",
                mime="text/csv"
            )
    except FileNotFoundError:
            st.info("Save your progress first to download it.")
    st.subheader("Saved Study History")

    try:
            with open("study_progress.csv", "r", newline="") as file:
                reader = csv.reader(file)
                history = list(reader)

            if history:
                for record in history:
                    st.write(
                        f"Date: {record[0]} | Subject: {record[2]} | "
                        f"Completed: {record[3]}/{record[4]}"
                    )
            else:
                st.info("No saved progress yet.")

    except FileNotFoundError:
            st.info("Save your progress first to see your history.")
    if st.button("Save My Progress"):
            with open("study_progress.csv", "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    name,
                    subject,
                    completed,
                    len(tasks)
                ])

            st.success("Your progress has been saved!")
    else:
        st.warning("Please fill in your name, subject, and goal.")