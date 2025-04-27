import sys
import os
import pytest
from datetime import datetime, timedelta

# Fix path to import tasks module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import tasks

# =============================
# Test generate_unique_id
# =============================

def test_generate_unique_id_empty_list():
    empty_tasks = []
    assert tasks.generate_unique_id(empty_tasks) == 1

def test_generate_unique_id_with_existing_tasks():
    sample_tasks = [{"id": 1}, {"id": 2}, {"id": 5}]
    assert tasks.generate_unique_id(sample_tasks) == 6

# =============================
# Test filter_tasks_by_priority
# =============================

def test_filter_tasks_by_priority():
    sample_tasks = [
        {"id": 1, "priority": "High"},
        {"id": 2, "priority": "Medium"},
        {"id": 3, "priority": "High"},
    ]
    filtered = tasks.filter_tasks_by_priority(sample_tasks, "High")
    assert len(filtered) == 2
    for task in filtered:
        assert task["priority"] == "High"

# =============================
# Test filter_tasks_by_category
# =============================

def test_filter_tasks_by_category():
    sample_tasks = [
        {"id": 1, "category": "Work"},
        {"id": 2, "category": "Home"},
        {"id": 3, "category": "Work"},
    ]
    filtered = tasks.filter_tasks_by_category(sample_tasks, "Work")
    assert len(filtered) == 2
    for task in filtered:
        assert task["category"] == "Work"

# =============================
# Test filter_tasks_by_completion
# =============================

def test_filter_tasks_by_completion():
    sample_tasks = [
        {"id": 1, "completed": True},
        {"id": 2, "completed": False},
        {"id": 3, "completed": True},
    ]
    completed_tasks = tasks.filter_tasks_by_completion(sample_tasks, completed=True)
    assert len(completed_tasks) == 2
    for task in completed_tasks:
        assert task["completed"] is True

    incomplete_tasks = tasks.filter_tasks_by_completion(sample_tasks, completed=False)
    assert len(incomplete_tasks) == 1
    for task in incomplete_tasks:
        assert task["completed"] is False

# =============================
# Test search_tasks
# =============================

def test_search_tasks_title_and_description():
    sample_tasks = [
        {"id": 1, "title": "Buy groceries", "description": "Milk, Bread, Eggs"},
        {"id": 2, "title": "Finish project", "description": "Due Monday"},
        {"id": 3, "title": "Call plumber", "description": "Fix sink"},
    ]
    results = tasks.search_tasks(sample_tasks, "groceries")
    assert len(results) == 1
    assert results[0]["title"] == "Buy groceries"

    results = tasks.search_tasks(sample_tasks, "sink")
    assert len(results) == 1
    assert results[0]["title"] == "Call plumber"

    results = tasks.search_tasks(sample_tasks, "meeting")
    assert len(results) == 0

# =============================
# Test load_tasks
# =============================

def test_load_tasks_file_not_found(tmp_path):
    fake_file = tmp_path / "nonexistent.json"
    loaded_tasks = tasks.load_tasks(str(fake_file))
    assert loaded_tasks == []

def test_load_tasks_corrupt_json(tmp_path):
    bad_json_file = tmp_path / "bad_tasks.json"
    bad_json_file.write_text("{ this is not valid JSON }")
    loaded_tasks = tasks.load_tasks(str(bad_json_file))
    assert loaded_tasks == []

# =============================
# Test save_tasks
# =============================

def test_save_tasks(tmp_path):
    task_list = [{"id": 1, "title": "Test"}]
    save_path = tmp_path / "saved_tasks.json"

    tasks.save_tasks(task_list, str(save_path))

    with open(save_path, "r") as f:
        data = f.read()

    assert "Test" in data

# =============================
# Test get_overdue_tasks
# =============================

def test_get_overdue_tasks():
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    future_date = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")

    sample_tasks = [
        {"id": 1, "due_date": yesterday, "completed": False},
        {"id": 2, "due_date": future_date, "completed": False},
        {"id": 3, "due_date": yesterday, "completed": True},
    ]

    overdue = tasks.get_overdue_tasks(sample_tasks)
    assert len(overdue) == 1
    assert overdue[0]["id"] == 1