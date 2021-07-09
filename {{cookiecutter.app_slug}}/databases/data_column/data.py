from pathlib import Path
from contextlib import contextmanager
from typing import Any, Iterator, List, Optional

import duckdb

from ..models.task import Task


@contextmanager
def database_connection() -> Iterator[duckdb.DuckDBPyConnection]:
    connection: duckdb.DuckDBPyConnection = duckdb.connect(f"{Path(__file__).parent}/db.duckdb")    
    cursor: duckdb.DuckDBPyConnection = connection.cursor()
    try:
        yield cursor
        connection.commit()
    finally:
        cursor.close()
        connection.close()


def init_database():
    query = """DROP TABLE IF EXISTS tasks;
               DROP SEQUENCE IF EXISTS __id;
            """

    with database_connection() as db:
        db.execute(query)

    query = "CREATE SEQUENCE IF NOT EXISTS __id START 1;"

    with database_connection() as db:
        db.execute(query)

    query = """
                CREATE TABLE IF NOT EXISTS tasks (
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

    query = """INSERT INTO tasks (id, text, day, reminder) 
               VALUES (nextval('__id'), ?, ?, ?)"""

    parameters = [task.text, task.day, task.reminder]
    
    with database_connection() as db:
        db.execute(query, parameters)
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
               SET text = ?, day = ?, reminder = ?
               WHERE id = ?"""

    parameters = [task.text, task.day, task.reminder, task.id]

    with database_connection() as db:
        db.execute(query, parameters)

    return task
