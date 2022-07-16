from flask import Flask
from .config import SECRET_KEY
from .api.v1.routes.crud import crud


def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY=SECRET_KEY
    )

    app.register_blueprint(crud)

    return app
