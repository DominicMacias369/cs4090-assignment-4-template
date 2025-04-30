import sys
import os
import pytest
from datetime import datetime, timedelta

# Fix path to import tasks
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import tasks

def test_get_overdue_tasks():
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    sample_tasks = [
        {"id": 1, "title": "Past Task", "due_date": yesterday, "completed": False},
        {"id": 2, "title": "Future Task", "due_date": tomorrow, "completed": False},
        {"id": 3, "title": "Completed Past Task", "due_date": yesterday, "completed": True}
    ]

    overdue = tasks.get_overdue_tasks(sample_tasks)

    # Only Task 1 should be returned
    assert len(overdue) == 1
    assert overdue[0]["id"] == 1

def test_search_tasks():
    sample_tasks = [
        {"id": 1, "title": "Write report", "description": "Write the TDD section"},
        {"id": 2, "title": "Meeting", "description": "Zoom with professor"},
        {"id": 3, "title": "Buy milk", "description": "Go to grocery store"}
    ]

    result = tasks.search_tasks(sample_tasks, "report")
    assert len(result) == 1
    assert result[0]["id"] == 1

    result = tasks.search_tasks(sample_tasks, "zoom")
    assert len(result) == 1
    assert result[0]["id"] == 2

    result = tasks.search_tasks(sample_tasks, "grocery")
    assert len(result) == 1
    assert result[0]["id"] == 3

    result = tasks.search_tasks(sample_tasks, "nothing")
    assert len(result) == 0

def test_summarize_by_category():
    sample_tasks = [
        {"id": 1, "category": "Work"},
        {"id": 2, "category": "Personal"},
        {"id": 3, "category": "Work"},
        {"id": 4, "category": "School"},
        {"id": 5, "category": "Work"},
    ]

    result = tasks.summarize_by_category(sample_tasks)
    assert result == {"Work": 3, "Personal": 1, "School": 1}
