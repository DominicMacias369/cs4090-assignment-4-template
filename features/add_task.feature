Feature: To-Do List Behaviors

  Scenario: Add a task and confirm it appears
    Given the task list is empty
    When I add a task titled "Read book" with category "Personal"
    Then the task list should contain 1 task titled "Read book"

  Scenario: Mark a task as completed
    Given a task titled "Write report" is incomplete
    When I mark the task "Write report" as complete
    Then the task "Write report" should be marked as completed

  Scenario: Delete a task
    Given a task titled "Buy milk" exists
    When I delete the task titled "Buy milk"
    Then the task list should not contain "Buy milk"

  Scenario: Filter tasks by priority
    Given multiple tasks with different priorities
    When I filter tasks by "High" priority
    Then only tasks with "High" priority should be returned

  Scenario: Filter overdue tasks only
    Given some tasks are overdue
    When I filter for overdue tasks
    Then only overdue tasks should be returned
