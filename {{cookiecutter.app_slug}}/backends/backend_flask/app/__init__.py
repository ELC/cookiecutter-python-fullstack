from flask import Flask

from .data import data
from .routes import api_routes, ui_routes, error_routes

{% if cookiecutter.app_frontend == "react" -%}
app = Flask(__name__)
{%- elif cookiecutter.app_frontend in ["angular", "vue"] -%}
app = Flask(__name__, static_url_path="")
{%- endif %}


app.register_blueprint(api_routes, url_prefix="/")
# app.register_blueprint(error_routes, url_prefix="/")
app.register_blueprint(ui_routes, url_prefix="/")

data.init_database()
