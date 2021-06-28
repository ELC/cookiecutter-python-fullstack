from pathlib import Path
from contextlib import contextmanager
from typing import Any, Iterator, List, Optional

import ZODB, ZODB.FileStorage
from BTrees import OOBTree
import transaction

from ..models.task import Task


@contextmanager
def database_connection() -> Iterator[Any]:
    connection = ZODB.connection(f"{Path(__file__).parent}/db.fs")
    root = connection.root
    try:
        yield root
        transaction.commit()
    finally:
        connection.close()


def init_database():
    init_data = [
        Task(id=1, text="Doctors Appointment", day="Feb 5th at 2:30pm", reminder=True),
        Task(id=2, text="Meeting at School", day="Feb 6th at 1:30pm", reminder=True),
    ]

    with database_connection() as db:
        db.tasks = OOBTree.BTree()

        for task in init_data:
            db.tasks[task.id] = task


def insert_taks(task: Task) -> Task:
    task_dict = task._asdict()

    with database_connection() as db:
        new_id = db.tasks.maxKey() + 1
        task_dict["id"] = new_id
        new_task = Task(**task_dict)
        db.tasks[new_task.id] = new_task

    return new_task


def get_all() -> List[Task]:
    with database_connection() as db:
        tasks = list(db.tasks.values())

    return tasks


def get_by_id(task: Task) -> Optional[Task]:

    with database_connection() as db:
        record = db.tasks[task.id] if task.id in db.tasks else None

    return record


def delete_by_id(task: Task) -> None:
    with database_connection() as db:
        if task.id in db.tasks:
            del db.tasks[task.id]


def update_by_id(task: Task) -> Task:
    with database_connection() as db:
        db.tasks[task.id] = task

    return task
