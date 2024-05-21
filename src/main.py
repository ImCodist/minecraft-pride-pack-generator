"""
Starts the web server and initializes any assets that need to be
referenced frequently by users.
This should always be called when you want to actually start the application.
"""


import web


def main():
    app = web.create_app()
    app.run(debug=True)


if __name__ == "__main__":
    main()