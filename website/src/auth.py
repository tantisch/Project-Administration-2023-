from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from src.models import UserDatabase

auth = Blueprint("auth", __name__)


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
            return render_template("login.html", user=current_user)

        # for development purposes
        elif ":" not in user.password and user.password == user_password:
            login_user(user, remember=True)
            return redirect(url_for("views.main"))

        # incorrect password
        elif not check_password_hash(user.password, user_password):
            flash("Не правильний пароль.", category="error")
            return render_template("login.html", user=current_user)

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
