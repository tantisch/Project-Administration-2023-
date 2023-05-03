from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from src.auth import User

views = Blueprint("views", __name__)


# page with general access
@views.route("/")
@views.route("/main.html")
def main():
    if current_user.is_authenticated:
        if current_user.role_id == 1:
            return redirect(url_for('views.owner'))
        elif current_user.role_id == 2:
            return redirect(url_for('views.director'))
        elif current_user.role_id == 3:
            return redirect(url_for('views.driver'))
        elif current_user.role_id == 4:
            flash("Ви успішно увійшли в акаунт, але вам ще не назначено ролі.", category="info")
            return redirect(url_for('auth.login'))
    else:
        return render_template("main.html")


# page with general access
# @views.route("/faqs.html")
# def faqs():
#     return render_template("faqs.html")


# page with general access
@views.route("/contact.html")
def contact_us():
    return render_template("contact.html")


# page with general access
# @views.route("/privacy-policy.html")
# def privacy_policy():
#     return render_template("privacy-policy.html")


# page with general access
# @views.route("/terms-of-service.html")
# def terms_of_service():
#     return render_template("terms-of-service.html")


# @views.route("/manage.html")
# def manage():
#     return render_template("manage.html")


@views.route("/owner.html")
@login_required
def owner():
    if current_user.role_id != 1:
        return redirect(url_for("views.main"))
    return render_template("owner.html")


@views.route("/director.html")
@login_required
def director():
    if current_user.role_id > 2:
        return redirect(url_for("views.main"))
    return render_template("director.html")


@views.route("/driver.html")
@login_required
def driver():
    if current_user.role_id > 3:
        return redirect(url_for("views.main"))


    return render_template("driver.html")
