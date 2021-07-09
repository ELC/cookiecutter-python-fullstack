import sys
import shutil
import importlib
import json
from pathlib import Path

from cookiecutter.main import cookiecutter
import pytest

from common import PARAMS, OUTPUT_DIR, EXTRA as EXTRA_

overwrite_backend = dict(app_backend="flask")
EXTRA = dict(EXTRA_, **overwrite_backend)


@pytest.fixture(autouse=True)
def post_build():
    if Path(OUTPUT_DIR).is_dir():
        shutil.rmtree(OUTPUT_DIR)
    yield

    shutil.rmtree(OUTPUT_DIR)
    if OUTPUT_DIR in sys.path:
        sys.path.pop(sys.path.index(OUTPUT_DIR))


def get_client():
    if OUTPUT_DIR not in sys.path:
        sys.path.insert(0, OUTPUT_DIR)

    app_module = importlib.import_module(f"backend.app")
    app_module.data = importlib.reload(app_module.data)  # Avoid Caching database
    app_module.data.init_database()

    with app_module.app.test_client() as client:
        yield client


@pytest.mark.parametrize("database", ["SQL", "NoSQL (Column/OLAP)", "NoSQL (Column/OLAP)", "NoSQL (Document)", "NoSQL (Key-Value/Cache)", "Object-Based"])
def test_api(database):
    overwrite_database = dict(app_database=database)
    overwrite = dict(EXTRA, **overwrite_database)
    cookiecutter(".", extra_context=overwrite, **PARAMS)

    client = next(get_client())

    response = client.get("/echo/4")
    assert {"value": "4"} == response.json


def test_index():
    cookiecutter(".", extra_context=EXTRA, **PARAMS)

    client = next(get_client())

    response = client.get("/")
    assert "<noscript>You need to enable" in str(response.data)


@pytest.mark.parametrize("database", ["SQL", "NoSQL (Column/OLAP)", "NoSQL (Document)", "NoSQL (Key-Value/Cache)", "Object-Based"])
def test_data_get(database):
    overwrite_database = dict(app_database=database)
    overwrite = dict(EXTRA, **overwrite_database)
    cookiecutter(".", extra_context=overwrite, **PARAMS)

    client = next(get_client())

    response = client.get("/tasks/2")

    expected = {
        "id": 2,
        "text": "Meeting at School",
        "day": "Feb 6th at 1:30pm",
        "reminder": True,
    }
    assert expected == response.json


@pytest.mark.parametrize("database", ["SQL", "NoSQL (Column/OLAP)", "NoSQL (Document)", "NoSQL (Key-Value/Cache)", "Object-Based"])
def test_data_get_all(database):
    overwrite_database = dict(app_database=database)
    overwrite = dict(EXTRA, **overwrite_database)
    cookiecutter(".", extra_context=overwrite, **PARAMS)

    client = next(get_client())

    all_tasks = []

    for id_ in range(1, 3):
        task = client.get(f"/tasks/{id_}")
        all_tasks.append(task.json)

    get_all = client.get(f"/tasks")

    assert all_tasks == get_all.json


@pytest.mark.parametrize("database", ["SQL", "NoSQL (Column/OLAP)", "NoSQL (Document)", "NoSQL (Key-Value/Cache)", "Object-Based"])
def test_data_insert(database):
    overwrite_database = dict(app_database=database)
    overwrite = dict(EXTRA, **overwrite_database)
    cookiecutter(".", extra_context=overwrite, **PARAMS)

    client = next(get_client())

    new_task = {
        "text": "Study for Exam",
        "day": "Dec 10th at 5:30pm",
        "reminder": False,
    }

    count_before = len(client.get("/tasks").json)
    insert_respose = client.post("/tasks", data=json.dumps(new_task)).json

    del insert_respose["id"]
    assert new_task == insert_respose

    count_after = len(client.get("/tasks").json)

    assert count_before + 1 == count_after

    new_task_db = client.get("/tasks/3").json

    del new_task_db["id"]

    assert new_task == new_task_db

    new_task_db = client.get("/tasks/3").json

    new_task["id"] = 3

    assert new_task == new_task_db


@pytest.mark.parametrize("database", ["SQL", "NoSQL (Column/OLAP)", "NoSQL (Document)", "NoSQL (Key-Value/Cache)", "Object-Based"])
def test_data_delete(database):
    overwrite_database = dict(app_database=database)
    overwrite = dict(EXTRA, **overwrite_database)
    cookiecutter(".", extra_context=overwrite, **PARAMS)

    client = next(get_client())

    response = client.get("/tasks/2").json

    assert response != {}

    response = client.delete("/tasks/2")

    response = client.get("/tasks/2").json

    assert response == {}


@pytest.mark.parametrize("database", ["SQL", "NoSQL (Column/OLAP)", "NoSQL (Document)", "NoSQL (Key-Value/Cache)", "Object-Based"])
def test_data_update(database):
    overwrite_database = dict(app_database=database)
    overwrite = dict(EXTRA, **overwrite_database)
    cookiecutter(".", extra_context=overwrite, **PARAMS)

    client = next(get_client())

    task2_original = client.get("/tasks/2").json

    task2_modified = task2_original.copy()
    task2_modified["reminder"] = not task2_modified["reminder"]

    response = client.put("/tasks/2", data=json.dumps(task2_modified)).json

    assert task2_modified == response

    task2_updated = client.get("/tasks/2").json

    assert task2_original["reminder"] == (not task2_updated["reminder"])
