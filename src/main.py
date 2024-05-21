"""
Starts the web server and stores any important information.
This should always be run when you want to actually start the application.
"""


import web
import gitinfo


VERSION = (0, 0, 0)

# TODO: it could be cool to move some options users may wanna change if self hosting here


# setup versioning info
version_formatted = ".".join(map(str, VERSION))
git_info = gitinfo.get_git_info()


def main():
    app = web.create_app()
    app.run(debug=True)


if __name__ == "__main__":
    main()