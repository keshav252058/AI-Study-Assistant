import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:1b"


def ask_ai(question):
    """Send a question to the local Ollama AI model."""

    data = {
        "model": MODEL_NAME,
        "prompt": question,
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=data,
        timeout=180
    )

    response.raise_for_status()

    return response.json()["response"]


def create_study_plan(subject, goal, study_hours):
    """Create a basic study plan."""

    tasks = [
        f"Revise the basics of {subject}",
        f"Study topics related to your goal: {goal}",
        f"Practice questions related to {subject}",
        "Review what you learned today"
    ]

    return {
        "subject": subject,
        "goal": goal,
        "study_hours": study_hours,
        "tasks": tasks
    }


def generate_personalized_plan(subject, goal, study_hours):
    """Generate a personalized study plan using AI."""

    prompt = f"""
You are a helpful AI study coach.

Create a practical and beginner-friendly study plan.

Subject: {subject}
Student's goal: {goal}
Available study time per day: {study_hours} hours

Include:
1. A simple timetable.
2. Three specific study tasks.
3. A short revision activity.
4. One useful study tip.

Keep the response clear and easy to understand.
"""

    return ask_ai(prompt)


def study_agent():
    print("AI Study Assistant Agent")
    question = input("Ask your study question: ")

    try:
        answer = ask_ai(question)

        print("\nAI Assistant:")
        print(answer)

    except requests.exceptions.RequestException as error:
        print("\nCould not connect to Ollama.")
        print("Check that Ollama is running.")
        print(error)


if __name__ == "__main__":
    study_agent()