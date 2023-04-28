import time

from flask import Flask
from vertica_python.vertica.cursor import Cursor

import config
import vertica_python as vp

cursor: Cursor = None


def connect_to_database():
    failed_attempts_count = 0
    global cursor

    while True:
        try:
            conn_vc = vp.connect(**config.connect_vc)
        except Exception as e:
            failed_attempts_count += 1
            print(f"Error occurred during connection to database: {e}")
            time.sleep(5)
            if failed_attempts_count > 7:
                raise e
            continue

        cursor = conn_vc.cursor()
        break

    print("Connection to database was established successfully")


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = config.secret_key
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    return app
