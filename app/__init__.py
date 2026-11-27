from flask import Flask
from .db import init_db, close_db
from pathlib import Path

def create_app():
    app = Flask(__name__)

    app.config['DATABASE'] = Path(app.instance_path) / 'products.sqlite3'
    init_db(app)
    app.teardown_appcontext(close_db) # makes Flask call close_db after each HTTP-request

    from . import routes
    app.register_blueprint(routes.bp)
    app.register_blueprint(routes.api_bp)

    return app
