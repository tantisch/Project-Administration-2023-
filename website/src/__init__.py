import time

from flask import Flask

import config
import psycopg2
from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor

conn: Connection = None
cursor: Cursor = None


def connect_to_database():
    failed_attempts_count = 0
    max_failed_attempts_number = 7
    global conn, cursor

    while True:
        try:
            conn = psycopg2.connect(**config.connect_postgres)
        except Exception as e:
            failed_attempts_count += 1
            print(f"Error occurred during connection to database: {e}")
            time.sleep(5)
            if failed_attempts_count > max_failed_attempts_number:
                raise e
            continue

        cursor = conn.cursor()
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
