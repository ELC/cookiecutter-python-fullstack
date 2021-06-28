import shutil
import subprocess
from pathlib import Path

import pytest
from cookiecutter.main import cookiecutter

from common import EXTRA, PARAMS, OUTPUT_DIR


@pytest.fixture(autouse=True)
def post_build():
    if Path(OUTPUT_DIR).is_dir():
        shutil.rmtree(OUTPUT_DIR)
    yield

    try:
        container_build = subprocess.run(f"docker build --quiet {OUTPUT_DIR}/.")
        assert container_build.returncode == 0
    finally:
        shutil.rmtree(OUTPUT_DIR)


def test_defaults():
    cookiecutter(".", extra_context=EXTRA, **PARAMS)


@pytest.mark.parametrize("database", ["SQL", "NoSQL (Document)", "Object-Based"])
@pytest.mark.parametrize("frontend", ["vue", "react", "angular"])
@pytest.mark.parametrize("manager", ["pip", "pipenv"])
@pytest.mark.parametrize("webserver", ["waitress", "uwsgi"])
def test_flask(manager, webserver, frontend, database):
    overwrite_backend = dict(
        app_backend="flask",
        app_dependency_manager=manager,
        app_webserver=webserver,
        app_frontend=frontend,
        app_database=database,
    )
    overwrite = dict(EXTRA, **overwrite_backend)
    cookiecutter(".", extra_context=overwrite, **PARAMS)
