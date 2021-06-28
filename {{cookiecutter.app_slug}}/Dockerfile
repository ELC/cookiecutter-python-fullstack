############# Build Back End

{% if cookiecutter.app_python_version == "3.8" -%}
FROM python:3.8 as backend
{%- elif cookiecutter.app_python_version == "3.7" -%}
FROM python:3.7 as backend
{%- elif cookiecutter.app_python_version == "3.9" -%}
FROM python:3.9 as backend
{%- endif %}

RUN pip install --upgrade pip

WORKDIR /usr/src/

{% if cookiecutter.app_dependency_manager == "pip" %}
COPY backend/requirements.txt requirements.txt
RUN pip install --no-cache -r requirements.txt
{%- elif cookiecutter.app_dependency_manager == "pipenv" -%}
RUN pip install pipenv
COPY backend/Pipfile Pipfile
RUN pipenv install
{%- endif %}

COPY backend/ ./

############# Build Front-End

FROM node:12-alpine as frontend

WORKDIR /usr/src/

COPY frontend/package.json package.json
RUN npm install .

COPY frontend .
{% if cookiecutter.app_frontend in ["react", "vue"] -%}
COPY --from=backend /usr/src/app/templates public/
{%- elif cookiecutter.app_frontend == "angular" -%}
COPY --from=backend /usr/src/app/templates src/
{%- endif %}
RUN npm run build


############# Run Production

FROM backend as production

COPY --from=frontend /usr/src/build/index.html ./app/templates/
COPY --from=frontend /usr/src/build/ ./app/static/

{% if cookiecutter.app_frontend == "react" -%}
COPY --from=frontend /usr/src/build/static/ ./app/static/
{%- endif %}

# Run Production
EXPOSE {{ cookiecutter.app_port }}

{% if cookiecutter.app_webserver == "uwsgi" -%}
ENTRYPOINT ["uwsgi", "-s", "0.0.0.0:{{ cookiecutter.app_port }}", "--protocol=http", "--module", "app", "--callable", "app"]
{%- else -%}
ENTRYPOINT ["python", "-m", "app"]
{%- endif %}
