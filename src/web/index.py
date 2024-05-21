"""
The web application main page.
Where most of the controls are for the app.
"""


from flask import Blueprint, render_template


bp = Blueprint("index", __name__)


@bp.route("/")
def index():
    return render_template("index.html")