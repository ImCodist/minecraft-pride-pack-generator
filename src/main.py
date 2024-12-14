"""
Starts the web server and stores any important information.
This should always be run when you want to actually start the application.
"""


import web
import gitinfo


VERSION = (1, 1, 2)


# setup versioning info
version_formatted = ".".join(map(str, VERSION))
git_info = gitinfo.get_git_info()


def create_app():
    return web.create_app()


def main():
    app = web.create_app()
    app.run(debug=True)


if __name__ == "__main__":
    main()