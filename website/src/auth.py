import flask_login
import psycopg2.errors
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from src import cursor

auth = Blueprint("auth", __name__)


class User(UserMixin):
    # __slots__ = ["user_id", "user_email", "user_password", "role_id", "name", "surname", "surname2",
    #              "is_active", "is_authenticated"]

    def __init__(self, user_id: int = -1, role_id: int = 4, user_email: str = "", user_password: str = "",
                 name: str = "", surname: str = "", surname2: str = ""):
        """

        :param user_id:
        :param role_id: 1-'owner', 2-'director', 3-'driver', 4-'no-role'
        :param user_email:
        :param user_password:
        :param name:
        :param surname:
        :param surname2:
        """
        self.id = user_id
        self.role_id = role_id
        self.email = user_email
        self.password = user_password
        self.name = name
        self.surname = surname
        self.surname2 = surname2


class UserDatabase:
    db_cursor = cursor

    @staticmethod
    def add_user(user_email, user_password, role_id=4, name="", surname="", surname2=""):
        sql_query = f"""
                    insert into trolleybus_site_database.users (user_id, user_email, user_password, 
                    role_id, name, surname, surname2)
                    values (nextval('trolleybus_site_database.users_seq'), '{user_email}', 
                    '{user_password}', {role_id}, 
                    '{name}', '{surname}', '{surname2}');
                    """

        try:
            UserDatabase.db_cursor.execute(sql_query)
            UserDatabase.db_cursor.execute("commit;")
        except Exception as e:
            UserDatabase.db_cursor.execute("commit;")
            raise e

    @staticmethod
    def get_user_by_email(user_email) -> User:
        sql_query = f"""
                    select *
                    from trolleybus_site_database.users
                    where trolleybus_site_database.users.user_email = '{user_email}';
                    """

        UserDatabase.db_cursor.execute(sql_query)
        user_info = cursor.fetchone()

        if user_info is not None:
            user = User(*user_info)
        else:
            user = None
        return user

    @staticmethod
    def get_user_by_id(user_id) -> User:
        sql_query = f"""
                    select *
                    from trolleybus_site_database.users
                    where trolleybus_site_database.users.user_id = {user_id};
                    """

        UserDatabase.db_cursor.execute(sql_query)
        user_info = cursor.fetchone()

        if user_info is not None:
            user = User(*user_info)
        else:
            user = None
        return user


@auth.route("/register.html", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user_email = request.form.get("email")
        user_password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")

        user = UserDatabase.get_user_by_email(user_email)

        if user is not None:
            flash("Користувач з таким email вже існує. Введіть інший email.")
            return redirect(url_for('auth.register'))

        # TODO: add email verification using regexp
        if user_password != confirm_password:
            flash("Паролі не співпадають. Спробуйте ще.", category="error")
            return redirect(url_for("auth.register"))
        else:
            # user = User(email, generate_password_hash(password, method="scrypt"))
            UserDatabase.add_user(user_email=user_email,
                                  user_password=generate_password_hash(user_password, method="scrypt"))

            flash("Користувач був успішно створений!", category="info")
            user = UserDatabase.get_user_by_email(user_email)
            login_user(user, remember=True)
            return redirect(url_for("auth.login"))
    elif request.method == "GET":
        return render_template("register.html")


@auth.route("/login.html", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_email = request.form.get("email")
        user_password = request.form.get("password")

        user = UserDatabase.get_user_by_email(user_email)

        # incorrect email
        if user is None:
            flash("Користувача з вказаною поштою не існує.", category="error")
            return render_template("login.html", boolean=True)

        # incorrect password
        elif not check_password_hash(user.password, user_password):
            flash("Не правильний пароль.", category="error")
            return render_template("login.html", boolean=True)

        else:
            login_user(user, remember=True)
            return redirect(url_for("views.main"))

    elif request.method == "GET":

        return render_template("login.html", user=current_user)


@auth.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
