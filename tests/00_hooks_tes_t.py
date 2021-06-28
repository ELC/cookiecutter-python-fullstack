import shutil
from pathlib import Path
import os

import pytest
from cookiecutter.main import cookiecutter

from common import EXTRA, PARAMS, OUTPUT_DIR


@pytest.fixture(autouse=True)
def post_build():
    if Path(OUTPUT_DIR).is_dir():
        shutil.rmtree(OUTPUT_DIR)
    yield

    shutil.rmtree(OUTPUT_DIR)


def _backend_fronted(folders, type_):
    front_end_folders = [folder.stem for folder in folders if type_ in folder.stem]

    assert len(front_end_folders) == 1
    assert front_end_folders[0] == type_


@pytest.mark.parametrize("frontend", ["react", "angular", "vue"])
def test_folder_frontend(frontend):
    overwrite_backend = dict(app_frontend=frontend)
    overwrite = dict(EXTRA, **overwrite_backend)
    cookiecutter(".", extra_context=overwrite, **PARAMS)
    folders = [path for path in Path(OUTPUT_DIR).iterdir() if path.is_dir()]
    _backend_fronted(folders, "frontend")


@pytest.mark.parametrize("backend", ["flask"])
def test_folder_backend(backend):
    overwrite_backend = dict(app_backend=backend)
    overwrite = dict(EXTRA, **overwrite_backend)
    cookiecutter(".", extra_context=overwrite, **PARAMS)
    folders = [path for path in Path(OUTPUT_DIR).iterdir() if path.is_dir()]
    _backend_fronted(folders, "backend")


@pytest.mark.parametrize("database", ["SQL", "NoSQL (Document)", "NoSQL (Key-Value/Cache)", "Object-Based"])
def test_folder_database(database):
    overwrite_database = dict(app_database=database)
    overwrite = dict(EXTRA, **overwrite_database)
    cookiecutter(".", extra_context=overwrite, **PARAMS)
    folders = [
        path for path in Path(OUTPUT_DIR, "backend", "app").iterdir() if path.is_dir()
    ]
    _backend_fronted(folders, "data")

    if database == "NoSQL (Key-Value/Cache)":
        return

    data_path = Path(OUTPUT_DIR, "backend", "app", "data")
    extensions_in_data = [path.suffix for path in data_path.iterdir() if path.is_file()]

    all_formats = [".json", ".db", ".fs"]

    if database == "NoSQL (Document)":
        expected = ".json"
    elif database == "SQL":
        expected = ".db"
    elif database == "Object-Based":
        expected = ".fs"

    not_expected_formats = [format_ for format_ in all_formats if format_ != expected]

    assert expected in extensions_in_data
    assert all(
        not_expected not in extensions_in_data for not_expected in not_expected_formats
    )


def test_folder_data():
    cookiecutter(".", extra_context=EXTRA, **PARAMS)

    folders = [path.stem for path in Path(OUTPUT_DIR).iterdir() if path.is_dir()]
    assert all("data" not in path for path in folders)

    app_folder = Path(OUTPUT_DIR, "backend", "app")
    folders = [path for path in app_folder.iterdir()]
    _backend_fronted(folders, "data")


dependencies = {"pip": "requirements.txt", "pipenv": "Pipfile"}


@pytest.mark.parametrize("manager, required", dependencies.items())
def test_dependencies(manager, required):
    overwrite_dependency = dict(app_dependency_manager=manager)
    overwrite = dict(EXTRA, **overwrite_dependency)
    cookiecutter(".", extra_context=overwrite, **PARAMS)

    not_required = [file for type_, file in dependencies.items() if type_ != manager]

    found_required = False
    for _, _, files in os.walk(OUTPUT_DIR):
        for name in files:
            if name in not_required:
                assert False
            if name == required:
                found_required = True
    assert found_required
