import time

from flask import Flask
from flask_login import LoginManager

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
    connect_to_database()

    app = Flask(__name__)
    app.config["SECRET_KEY"] = config.secret_key

    from src.views import views
    from src.auth import auth
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from src.auth import UserDatabase

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Будь ласка увійдіть в акаунт, щоб перейти на дану сторінку."
    login_manager.login_message_category = "warning"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return UserDatabase.get_user_by_id(int(user_id))

    return app
