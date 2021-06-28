from pathlib import Path
from contextlib import contextmanager
from typing import Any, Iterator, List, Optional
import shutil

import diskcache as dc

from ..models.task import Task

database_path = Path(Path(__file__).parent, "cache")

@contextmanager
def database_connection() -> Iterator[Any]:
    cache = dc.Cache(database_path)
    try:
        with cache.transact():
            yield cache
    finally:
        cache.close()


def init_database():
    init_data = [
        Task(id=1, text="Doctors Appointment", day="Feb 5th at 2:30pm", reminder=True),
        Task(id=2, text="Meeting at School", day="Feb 6th at 1:30pm", reminder=True),
    ]

    shutil.rmtree(database_path, ignore_errors=True)
    with database_connection() as db:
        db.clear()
        for task in init_data:
            db[task.id] = task


def insert_taks(task: Task) -> Task:
    task_dict = task._asdict()

    with database_connection() as db:
        new_id = max(list(db.iterkeys())) + 1
        task_dict["id"] = new_id
        new_task = Task(**task_dict)
        db[new_task.id] = new_task

    return new_task


def get_all() -> List[Task]:
    with database_connection() as db:
        tasks = [db[key] for key in db.iterkeys()]

    return tasks


def get_by_id(task: Task) -> Optional[Task]:

    with database_connection() as db:
        record = db.get(task.id, default=None)

    return record


def delete_by_id(task: Task) -> None:
    with database_connection() as db:
        if task.id in db:
            del db[task.id]


def update_by_id(task: Task) -> Task:
    with database_connection() as db:
        if task.id in db:
            db[task.id] = task

    return task
