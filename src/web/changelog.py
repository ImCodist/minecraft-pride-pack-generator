"""
The web applications changelog.
Generated changelog based on a markdown file.
"""


from flask import Blueprint, render_template
from markdown_it import MarkdownIt
from os import path


CHANGELOG_FILE = "CHANGELOG.md"


bp = Blueprint("changelog", __name__)

md = MarkdownIt()


changelog_data = ""
if path.exists(CHANGELOG_FILE):
    changelog_file = open(CHANGELOG_FILE, "r")
    changelog_data = changelog_file.read()
    changelog_file.close()


@bp.route("/changelog")
def changelog():
    return render_template("changelog.html", changelog_html=md.render(changelog_data))