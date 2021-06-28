from contextlib import suppress

from invoke import task, run

@task
def test(context):
    run("pytest -svv")


@task
def cookie(context):
    run("cookiecutter --no-input --overwrite-if-exists . ")
    print("Successfully Cut the Cookie")


@task
def build(context):
    run("docker build --quiet --tag example example-app")
    print("Successfully Built Container")

@task
def run_docker(context):
    run("docker run -d -p 5000:5000 example")

@task
def stop(context):
    with suppress(Exception):
        run("docker stop example")
        run("docker rm example")

@task
def e2e(context):
    cookie(context)
    stop(context)
    build(context)
    run_docker(context)
