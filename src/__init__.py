from flask import Flask
from .config import SECRET_KEY
from .api.v1.routes.crud import crud
from flask_cors import CORS


def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY=SECRET_KEY
    )

    CORS(app, supports_credentials=True, resources={
        r"/*": {
            "origins": {
                "*",
            }
        }
    })


    app.register_blueprint(crud)

    return app
