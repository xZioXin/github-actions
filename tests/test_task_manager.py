import pytest
from datetime import date

from app.task_manager import TaskManager


def test_add_task():
    manager = TaskManager()

    task = manager.add_task(
        title="Prepare GitHub Actions project",
        priority=5,
        deadline=date(2026, 5, 10)
    )

    assert task.title == "Prepare GitHub Actions project"
    assert task.priority == 5
    assert task.completed is False
    assert len(manager.tasks) == 1


def test_add_task_with_empty_title():
    manager = TaskManager()

    with pytest.raises(ValueError):
        manager.add_task("", 3, date(2026, 5, 10))


def test_add_task_with_invalid_priority():
    manager = TaskManager()

    with pytest.raises(ValueError):
        manager.add_task("Invalid task", 10, date(2026, 5, 10))


def test_complete_task():
    manager = TaskManager()
    manager.add_task("Write tests", 4, date(2026, 5, 10))

    task = manager.complete_task("Write tests")

    assert task.completed is True


def test_complete_unknown_task():
    manager = TaskManager()

    with pytest.raises(ValueError):
        manager.complete_task("Unknown task")


def test_get_active_tasks():
    manager = TaskManager()
    manager.add_task("Task 1", 2, date(2026, 5, 10))
    manager.add_task("Task 2", 3, date(2026, 5, 11))

    manager.complete_task("Task 1")

    active_tasks = manager.get_active_tasks()

    assert len(active_tasks) == 1
    assert active_tasks[0].title == "Task 2"


def test_get_completed_tasks():
    manager = TaskManager()
    manager.add_task("Task 1", 2, date(2026, 5, 10))

    manager.complete_task("Task 1")

    completed_tasks = manager.get_completed_tasks()

    assert len(completed_tasks) == 1
    assert completed_tasks[0].title == "Task 1"


def test_get_overdue_tasks():
    manager = TaskManager()
    manager.add_task("Old task", 5, date(2026, 4, 20))
    manager.add_task("Future task", 3, date(2026, 6, 1))

    overdue_tasks = manager.get_overdue_tasks(date(2026, 5, 1))

    assert len(overdue_tasks) == 1
    assert overdue_tasks[0].title == "Old task"


def test_completed_task_is_not_overdue():
    manager = TaskManager()
    manager.add_task("Old task", 5, date(2026, 4, 20))

    manager.complete_task("Old task")
    overdue_tasks = manager.get_overdue_tasks(date(2026, 5, 1))

    assert len(overdue_tasks) == 0


def test_get_tasks_by_priority():
    manager = TaskManager()
    manager.add_task("Important task", 5, date(2026, 5, 10))
    manager.add_task("Normal task", 3, date(2026, 5, 11))

    priority_tasks = manager.get_tasks_by_priority(5)

    assert len(priority_tasks) == 1
    assert priority_tasks[0].title == "Important task"


def test_sort_by_deadline():
    manager = TaskManager()
    manager.add_task("Second task", 3, date(2026, 5, 20))
    manager.add_task("First task", 4, date(2026, 5, 10))

    sorted_tasks = manager.sort_by_deadline()

    assert sorted_tasks[0].title == "First task"
    assert sorted_tasks[1].title == "Second task"
