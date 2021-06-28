from . import app

{% if cookiecutter.app_webserver == "waitress" -%}
from waitress import serve

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port={{cookiecutter.app_port}}, threads=1)

{% else %}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port={{cookiecutter.app_port}}, debug=True)

{%- endif %}
