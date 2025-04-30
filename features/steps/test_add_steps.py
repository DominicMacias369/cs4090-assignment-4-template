import os
import sys
from datetime import datetime, timedelta
from pytest_bdd import scenarios, given, when, then

# Fix Python path so we can import from src/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
import tasks

# Load the Gherkin scenarios
scenarios('../add_task.feature')

# Use absolute path for isolated BDD testing file
TASKS_FILE = os.path.abspath("features/test_tasks.json")

# -----------------------------------------
# Scenario 1: Add a task and confirm it appears
# -----------------------------------------

@given("the task list is empty")
def given_empty_task_list():
    if os.path.exists(TASKS_FILE):
        os.remove(TASKS_FILE)
    tasks.save_tasks([], file_path=TASKS_FILE)

@when('I add a task titled "Read book" with category "Personal"')
def when_add_task():
    task_list = tasks.load_tasks(file_path=TASKS_FILE)
    task_list.append({
        "id": 1,
        "title": "Read book",
        "description": "Read a new novel",
        "priority": "Medium",
        "category": "Personal",
        "due_date": "2099-01-01",
        "completed": False,
        "created_at": "2099-01-01 12:00:00"
    })
    tasks.save_tasks(task_list, file_path=TASKS_FILE)

@then('the task list should contain 1 task titled "Read book"')
def then_check_task_present():
    task_list = tasks.load_tasks(file_path=TASKS_FILE)
    assert len(task_list) == 1
    assert task_list[0]["title"] == "Read book"

# -----------------------------------------
# Scenario 2: Mark a task as completed
# -----------------------------------------

@given('a task titled "Write report" is incomplete')
def given_incomplete_task():
    tasks.save_tasks([
        {
            "id": 1,
            "title": "Write report",
            "description": "Write the assignment",
            "priority": "Medium",
            "category": "School",
            "due_date": "2099-01-01",
            "completed": False,
            "created_at": "2099-01-01 12:00:00"
        }
    ], file_path=TASKS_FILE)

@when('I mark the task "Write report" as complete')
def when_complete_task():
    task_list = tasks.load_tasks(file_path=TASKS_FILE)
    for t in task_list:
        if t["title"] == "Write report":
            t["completed"] = True
    tasks.save_tasks(task_list, file_path=TASKS_FILE)

@then('the task "Write report" should be marked as completed')
def then_check_task_completed():
    task_list = tasks.load_tasks(file_path=TASKS_FILE)
    assert task_list[0]["completed"] is True

# -----------------------------------------
# Scenario 3: Delete a task
# -----------------------------------------

@given('a task titled "Buy milk" exists')
def given_task_to_delete():
    tasks.save_tasks([
        {
            "id": 1,
            "title": "Buy milk",
            "description": "Grocery run",
            "priority": "Low",
            "category": "Personal",
            "due_date": "2099-01-01",
            "completed": False,
            "created_at": "2099-01-01 12:00:00"
        }
    ], file_path=TASKS_FILE)

@when('I delete the task titled "Buy milk"')
def when_delete_task():
    task_list = tasks.load_tasks(file_path=TASKS_FILE)
    task_list = [t for t in task_list if t["title"] != "Buy milk"]
    tasks.save_tasks(task_list, file_path=TASKS_FILE)

@then('the task list should not contain "Buy milk"')
def then_task_removed():
    task_list = tasks.load_tasks(file_path=TASKS_FILE)
    assert all(t["title"] != "Buy milk" for t in task_list)

# -----------------------------------------
# Scenario 4: Filter tasks by priority
# -----------------------------------------

@given("multiple tasks with different priorities")
def given_priority_tasks():
    tasks.save_tasks([
        {"id": 1, "title": "Low", "priority": "Low", "category": "Work", "due_date": "2099-01-01", "completed": False, "created_at": "2099"},
        {"id": 2, "title": "Medium", "priority": "Medium", "category": "Work", "due_date": "2099-01-01", "completed": False, "created_at": "2099"},
        {"id": 3, "title": "High", "priority": "High", "category": "Work", "due_date": "2099-01-01", "completed": False, "created_at": "2099"},
    ], file_path=TASKS_FILE)

@when('I filter tasks by "High" priority')
def when_filter_high_priority():
    global filtered_tasks
    all_tasks = tasks.load_tasks(file_path=TASKS_FILE)
    filtered_tasks = tasks.filter_tasks_by_priority(all_tasks, "High")

@then('only tasks with "High" priority should be returned')
def then_only_high_tasks():
    assert all(task["priority"] == "High" for task in filtered_tasks)

# -----------------------------------------
# Scenario 5: Filter overdue tasks only
# -----------------------------------------

@given("some tasks are overdue")
def given_overdue_tasks():
    today = datetime.now().strftime("%Y-%m-%d")
    past = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")
    future = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
    tasks.save_tasks([
        {"id": 1, "title": "Past Task", "due_date": past, "completed": False, "priority": "Low", "category": "Work", "created_at": today},
        {"id": 2, "title": "Future Task", "due_date": future, "completed": False, "priority": "Low", "category": "Work", "created_at": today}
    ], file_path=TASKS_FILE)

@when("I filter for overdue tasks")
def when_filter_overdue():
    global filtered_overdue
    all_tasks = tasks.load_tasks(file_path=TASKS_FILE)
    filtered_overdue = tasks.get_overdue_tasks(all_tasks)

@then("only overdue tasks should be returned")
def then_check_overdue():
    today = datetime.now().strftime("%Y-%m-%d")
    assert all(task["due_date"] < today and not task["completed"] for task in filtered_overdue)
