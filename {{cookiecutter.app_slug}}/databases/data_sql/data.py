import sqlite3
from pathlib import Path
from contextlib import contextmanager
from typing import Any, Iterator, List, Optional

from ..models.task import Task


@contextmanager
def database_connection() -> Iterator[sqlite3.Cursor]:
    connection: sqlite3.Connection = sqlite3.connect(f"{Path(__file__).parent}/db.db")
    cursor: sqlite3.Cursor = connection.cursor()
    try:
        yield cursor
        connection.commit()
    finally:
        cursor.close()
        connection.close()


def init_database():
    query = "DROP TABLE IF EXISTS tasks"

    with database_connection() as db:
        db.execute(query)

    query = """CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY, 
                text TEXT, 
                day TEXT, 
                reminder INTEGER
               )"""

    with database_connection() as db:
        db.execute(query)

    init_data = [
        Task(id=1, text="Doctors Appointment", day="Feb 5th at 2:30pm", reminder=True),
        Task(id=2, text="Meeting at School", day="Feb 6th at 1:30pm", reminder=True),
    ]

    for task in init_data:
        insert_taks(task)


def insert_taks(task: Task) -> Task:
    task_dict = task._asdict()

    query = """INSERT INTO tasks (text, day, reminder) 
               VALUES (:text, :day, :reminder)"""

    with database_connection() as db:
        db.execute(query, task_dict)
        id_ = db.lastrowid

    task_dict["id"] = id_

    return Task(**task_dict)


def get_all() -> List[Task]:
    query = "SELECT id, text, day, reminder FROM tasks"

    with database_connection() as db:
        db.execute(query)
        records = db.fetchall()

    tasks = []
    for record in records:
        task = Task(
            id=record[0], text=record[1], day=record[2], reminder=bool(record[3])
        )
        tasks.append(task)

    return tasks


def get_by_id(task: Task) -> Optional[Task]:
    query = "SELECT id, text, day, reminder FROM tasks WHERE id = ?"
    parameters = [task.id]

    with database_connection() as db:
        db.execute(query, parameters)
        record = db.fetchone()

    if not record:
        return None

    return Task(id=record[0], text=record[1], day=record[2], reminder=bool(record[3]))


def delete_by_id(task: Task) -> None:
    query = "DELETE FROM tasks WHERE id = ?"
    parameters = [task.id]

    with database_connection() as db:
        db.execute(query, parameters)


def update_by_id(task: Task) -> Task:
    query = """UPDATE tasks 
               SET text = :text, day = :day, reminder = :reminder
               WHERE id = :id"""

    parameters = task._asdict()

    with database_connection() as db:
        db.execute(query, parameters)

    return task
