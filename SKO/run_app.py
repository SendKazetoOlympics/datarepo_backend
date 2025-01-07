import os

from flask import Flask
from flask_cors import CORS


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    from . import database, webhook, minio, nutrition
    app.register_blueprint(database.database_service, url_prefix="/flask/database")
    app.register_blueprint(webhook.webhook_service, url_prefix="/flask/webhook")
    app.register_blueprint(minio.minio_service, url_prefix="/flask/minio")
    app.register_blueprint(nutrition.nutrition_service, url_prefix="/flask/nutrition")

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
        app.config['SECRET_KEY']
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/flask/hello')
    def hello():
        return 'Hello, World!'

    CORS(app)

    return app

if __name__ == "__main__":
    app = create_app()
    CORS(app)
    app.run(host="0.0.0.0", port=9500)