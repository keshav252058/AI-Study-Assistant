print("Welcome to AI Study Assistant!")

name = input("What is your name? ")

print("Hello", name)
print("I am ready to help you study!")
subject = input("Which subject do you want to study? ")

print("Great", name + "!")
print("Let's study", subject)
goal = input("What is your study goal? ")

print("\nYour Study Plan")
print("Name:", name)
print("Subject:", subject)
print("Goal:", goal)
study_time = int(input("How many hours can you study today? "))

print("\nYour Study Plan")
print("Name:", name)
print("Subject:", subject)
print("Goal:", goal)
print("Available Study Time:", study_time, "hours")
print("\nYour Study Plan:")
def create_study_plan(subject, goal):
    print("\nYour Study Plan:")

    tasks = [
        "Revise the basics of " + subject,
        "Work on your goal: " + goal,
        "Practice questions related to " + subject,
        "Review what you learned today"
    ]

    for index, task in enumerate(tasks, start=1):
        print(index, ".", task)
    task_number = int(input("Enter completed task number (1-4): "))

    if 1 <= task_number <= len(tasks):
     completed_task = tasks.pop(task_number - 1)
    print("Completed:", completed_task)

    print("\nPending Tasks:")
    for task in tasks:
        print("-", task)
    else:
        print("Invalid task number")

create_study_plan(subject, goal)
total_minutes = study_time * 60

print("Your total study time is", total_minutes, "minutes.")
print("\nStudy Suggestion:")

if study_time <= 1:
    print("Focus on one important topic today.")
elif study_time <= 3:
    print("Study one topic and practice questions.")
else:
    print("Divide your time between revision, learning, and practice.")
def show_motivation():
    print("\nKeep learning!")
    print("Small progress every day leads to big results.")
show_motivation()