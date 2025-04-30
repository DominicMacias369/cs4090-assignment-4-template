import os
import sys

# Fix Python path to ensure 'src' is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import tasks

from hypothesis import given, settings, HealthCheck
from hypothesis.strategies import lists, dictionaries, text, sampled_from, booleans, integers

# ----------------------------------------
# Test 1: filter_tasks_by_priority only returns correct priority
# ----------------------------------------
@given(
    task_list=lists(
        dictionaries(
            keys=sampled_from(["id", "title", "priority", "category", "due_date", "completed", "created_at"]),
            values=text(min_size=1)
        ),
        min_size=1, max_size=10
    )
)
def test_filter_tasks_by_priority_property(task_list):
    for task in task_list:
        task.setdefault("priority", "Medium")
    filtered = tasks.filter_tasks_by_priority(task_list, "High")
    assert all(t["priority"] == "High" for t in filtered)

# ----------------------------------------
# Test 2: search_tasks only returns items that contain the query
# ----------------------------------------
@given(
    task_list=lists(
        dictionaries(
            keys=sampled_from(["title", "description"]),
            values=text(min_size=1)
        ),
        min_size=1, max_size=10
    ),
    query=text(min_size=1, max_size=5)
)
def test_search_tasks_property(task_list, query):
    result = tasks.search_tasks(task_list, query)
    for task in result:
        combined = task.get("title", "").lower() + task.get("description", "").lower()
        assert query.lower() in combined

# ----------------------------------------
# Test 3: get_overdue_tasks returns only past-due and not completed
# ----------------------------------------
@given(
    task_list=lists(
        dictionaries(
            keys=sampled_from(["due_date", "completed"]),
            values=text(min_size=1)
        ),
        min_size=1, max_size=10
    )
)
def test_get_overdue_tasks_property(task_list):
    for t in task_list:
        t.setdefault("due_date", "2000-01-01")  # force past
        t.setdefault("completed", False)
    overdue = tasks.get_overdue_tasks(task_list)
    for task in overdue:
        assert task["due_date"] < "2100-01-01"
        assert task["completed"] is False

# ----------------------------------------
# Test 4: save_tasks followed by load_tasks gives back same tasks
# ----------------------------------------
# Bypass health check
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(
    task_list=lists(
        dictionaries(
            keys=sampled_from(["id", "title", "priority", "category", "due_date", "completed", "created_at"]),
            values=text(min_size=1)
        ),
        min_size=1, max_size=10
    )
)
def test_save_load_roundtrip(tmp_path, task_list):
    file_path = tmp_path / "roundtrip.json"
    tasks.save_tasks(task_list, file_path=str(file_path))
    loaded = tasks.load_tasks(file_path=str(file_path))
    assert loaded == task_list

# ----------------------------------------
# Test 5: generate_unique_id always returns unused ID
# ----------------------------------------
@given(
    ids=lists(integers(min_value=1, max_value=1000), unique=True, min_size=1, max_size=20)
)
def test_generate_unique_id_property(ids):
    task_list = [{"id": i} for i in ids]
    new_id = tasks.generate_unique_id(task_list)
    existing_ids = [t["id"] for t in task_list]
    assert new_id not in existing_ids
