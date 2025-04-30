import pytest
import sys
import os

# Fix path to import tasks module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import tasks
from unittest import mock

# =============================
# Parametrized test for priority filtering
# =============================

@pytest.mark.parametrize("priority,expected_ids", [
    ("High", [1]),
    ("Medium", [2]),
    ("Low", [3]),
])
def test_filter_tasks_by_priority_parametrized(priority, expected_ids):
    sample_tasks = [
        {"id": 1, "priority": "High"},
        {"id": 2, "priority": "Medium"},
        {"id": 3, "priority": "Low"},
    ]
    filtered = tasks.filter_tasks_by_priority(sample_tasks, priority)
    result_ids = [task["id"] for task in filtered]
    assert result_ids == expected_ids

# =============================
# Mocking test for save_tasks
# =============================

def test_save_tasks_mock_open():
    sample_tasks = [{"id": 1, "title": "Mock Task"}]

    with mock.patch("builtins.open", mock.mock_open()) as mocked_file:
        tasks.save_tasks(sample_tasks, "fake_tasks.json")
        
        # Assert that open was called correctly
        mocked_file.assert_called_once_with("fake_tasks.json", "w")
        
        # You can also check that write() was called inside if you want to be thorough
        handle = mocked_file()
        handle.write.assert_called()