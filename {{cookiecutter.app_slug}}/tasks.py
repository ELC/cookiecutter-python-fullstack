from invoke import task, run
import shutil
from distutils import dir_util


@task
def backend(context):
    print("####### BUILDING BACKEND #######")
    {% if cookiecutter.app_dependency_manager == "pip" -%}
    run("pip install -r backend/requirements.txt")
    {%- elif cookiecutter.app_dependency_manager == "pipenv" -%}
    run("cd backend && pipenv install")
    {%- endif %}


@task
def frontend(context):
    print("####### BUILDING FRONTEND #######")
    run("cd frontend && npm install")
    {% if cookiecutter.app_frontend in ["react", "vue"] -%}
    dir_util.copy_tree("backend/app/templates/", "frontend/public/")
    {%- elif cookiecutter.app_frontend == "angular" -%}
    dir_util.copy_tree("backend/app/templates/", "frontend/src/")
    {%- endif %}
    run("cd frontend && npm run build")


@task
def production(context):
    print("####### PREPARE PRODUCTION BUILD #######")
    shutil.copy("frontend/build/index.html", "backend/app/templates/index.html")
    dir_util.copy_tree("frontend/build/", "backend/app/static/")
    {% if cookiecutter.app_frontend == "react" -%}
    dir_util.copy_tree("frontend/build/static/", "backend/app/static/")
    {%- endif %}
    

@task
def build(context):
    backend(context)
    frontend(context)
    production(context)


@task
def serve(context):
    print("####### RUN WEB SERVER #######")
    {% if cookiecutter.app_webserver == "uwsgi" -%}
    run("cd backend && uwsgi -s 0.0.0.0:{{ cookiecutter.app_port }} --protocol=http --module app --callable app")
    {%- else -%}
    run("cd backend && python -m app")
    {%- endif %}


@task
def buildAndServe(context):
    build(context)
    serve(context)
