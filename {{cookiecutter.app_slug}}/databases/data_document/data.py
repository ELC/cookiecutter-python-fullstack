from typing import List, Optional
from pathlib import Path

from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage

from contextlib import contextmanager

from ..models.task import Task

DATABASE_PARAMS = dict(storage=JSONStorage, indent=4, separators=(",", ": "))


@contextmanager
def database_connection():
    db = TinyDB(f"{Path(__file__).parent}/db.json", **DATABASE_PARAMS)
    db.default_table_name = "tasks"

    try:
        yield db
    finally:
        db.close()


def init_database():
    init_data = [
        {
            "id": 1,
            "text": "Doctors Appointment",
            "day": "Feb 5th at 2:30pm",
            "reminder": True,
        },
        {
            "id": 2,
            "text": "Meeting at School",
            "day": "Feb 6th at 1:30pm",
            "reminder": True,
        },
    ]

    db = TinyDB(f"{Path(__file__).parent}/db.json", **DATABASE_PARAMS)
    db.default_table_name = "tasks"
    db.truncate()

    with db:
        for document in init_data:
            db.insert(document)


def insert_taks(task: Task) -> Task:
    task_dict = task._asdict()

    if task.id == -1:
        new_id = max(get_all(), key=lambda x: x.id).id + 1
        task_dict["id"] = new_id

    with database_connection() as db:
        db.insert(task_dict)

    return Task(**task_dict)


def get_all() -> List[Task]:
    with database_connection() as db:
        results = db.all()
    return [Task(**task) for task in results]


def get_by_id(task: Task) -> Optional[Task]:
    Task_ = Query()

    with database_connection() as db:
        results = db.search(Task_.id == task.id)

    if not results:
        return None

    return Task(**results[0])


def delete_by_id(task: Task) -> None:
    Task_ = Query()

    with database_connection() as db:
        db.remove(Task_.id == task.id)


def update_by_id(task: Task) -> Task:
    Task_ = Query()

    with database_connection() as db:
        db.update(task._asdict(), Task_.id == task.id)

    return task
