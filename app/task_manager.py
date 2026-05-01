from dataclasses import dataclass
from datetime import date
from typing import List


@dataclass
class Task:
    title: str
    priority: int
    deadline: date
    completed: bool = False

    def mark_completed(self):
        self.completed = True

    def is_overdue(self, today: date):
        return not self.completed and self.deadline < today


class TaskManager:
    def __init__(self):
        self.tasks: List[Task] = []

    def add_task(self, title: str, priority: int, deadline: date):
        if not title.strip():
            raise ValueError("Title cannot be empty")

        if priority < 1 or priority > 5:
            raise ValueError("Priority must be from 1 to 5")

        task = Task(title, priority, deadline)
        self.tasks.append(task)
        return task

    def complete_task(self, title: str):
        for task in self.tasks:
            if task.title == title:
                task.mark_completed()
                return task
        raise ValueError("Task not found")

    def get_active_tasks(self):
        return [task for task in self.tasks if not task.completed]

    def get_completed_tasks(self):
        return [task for task in self.tasks if task.completed]

    def get_overdue_tasks(self, today: date):
        return [task for task in self.tasks if task.is_overdue(today)]

    def get_tasks_by_priority(self, priority: int):
        return [task for task in self.tasks if task.priority == priority]

    def sort_by_deadline(self):
        return sorted(self.tasks, key=lambda task: task.deadline)
