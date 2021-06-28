from flask import Blueprint, render_template

blueprint = Blueprint("ui", __name__)


@blueprint.route("/", methods=["GET"])
def index():
    return render_template("index.html")
