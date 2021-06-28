from typing import Union
from flask import Blueprint, jsonify, Response, request

from ..models.task import Task
from ..data import data

blueprint = Blueprint("api", __name__)


@blueprint.get("/echo/<value>")
def echo(value: str) -> Response:
    return jsonify({"value": value})


@blueprint.get("/tasks")
def get_all_tasks() -> Response:
    results = data.get_all()
    return jsonify([task._asdict() for task in results])


@blueprint.get("/tasks/<id>")
def get_tasks_by_id(id: Union[int, str]) -> Response:
    task = Task(id=int(id))
    result = data.get_by_id(task)

    if not result:
        return jsonify({})

    return jsonify(result._asdict())


@blueprint.post("/tasks")
def insert_new_task() -> Response:
    task = request.get_json(force=True) or {}

    if "id" not in task:
        task["id"] = -1

    new_task = Task(**task)
    new_task = data.insert_taks(new_task)
    return jsonify(new_task._asdict())


@blueprint.delete("/tasks/<id>")
def delete_tasks_by_id(id: Union[int, str]) -> Response:
    task = Task(id=int(id))
    data.delete_by_id(task)
    return jsonify({"Message": "OK"})


@blueprint.put("/tasks/<id>")
def update_tasks_by_id(id: Union[int, str]) -> Response:
    task = request.get_json(force=True) or {}
    task["id"] = int(id)
    task = Task(**task)
    updated_task = data.update_by_id(task)
    return jsonify(updated_task._asdict())
