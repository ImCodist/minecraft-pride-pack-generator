"""
All web server related code exists here.
Like initializing the web server and running code from requests and stuffs.
"""


from os import path
from flask import Flask


def create_app():
    app = Flask(
        __name__,
        static_folder=path.abspath("web/static"),
        template_folder=path.abspath("web/templates")
    )
    
    
    from web.index import bp as bp_index
    app.register_blueprint(bp_index)
    
    from web.changelog import bp as bp_changelog
    app.register_blueprint(bp_changelog)
    
    
    from web.generate import bp as bp_generate
    app.register_blueprint(bp_generate)
    
    from web.data import bp as bp_data
    app.register_blueprint(bp_data)
    
    from web.assets import bp as bp_assets
    app.register_blueprint(bp_assets)
    
    return app
