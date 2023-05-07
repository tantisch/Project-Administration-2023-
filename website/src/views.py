from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from src.models import DriverDatabase, Driver, User, DirectorDatabase

views = Blueprint("views", __name__)


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


@views.route("/faqs.html")
def faqs():
    return render_template("faqs.html")


@views.route("/contact.html")
def contact_us():
    return render_template("contact.html")


@views.route("/privacy_policy.html")
def privacy_policy():
    return render_template("privacy_policy.html")


@views.route("/terms_of_service.html")
def terms_of_service():
    return render_template("terms-of-service.html")


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


# @views.route("/driver.html?id=<string:driver_id>")
@views.route("/driver.html")
@login_required
def driver():
    if current_user.role_id > 3:
        return redirect(url_for("views.main"))

    driver_obj: Driver = None
    if current_user.role_id == 3:
        driver_obj = DriverDatabase.get_driver_by_driver_id(current_user.id)

    # director views driver account with url: "/driver.html?id=-3", where id is driver_id
    elif current_user.role_id == 2:
        driver_id = request.args.get("id")
        if driver_id is None:
            flash("Водій не вказаний", "error")
        else:
            driver_id = int(driver_id)

            driver_obj = DriverDatabase.get_driver_by_driver_id(driver_id)

    if driver_obj is not None:
        director_obj = DirectorDatabase.get_director_by_user_id(current_user.id)

        if driver_obj.director_id != director_obj.id:
            flash("Цей водій не призначений до вас, тому ви не можете переглянути інформацію про нього.", "warning")
            driver_obj = None
            return render_template("driver.html", driver_obj=driver_obj)

        driver_obj.stations = driver_obj.stations.split(driver_obj.station_delimiter)
        driver_obj.stations = [] if len(driver_obj.stations) == 1 and driver_obj.stations[0] == "" \
            else driver_obj.stations

        if not driver_obj.stations:
            flash("На сьогодні вам не призначено маршрут", "info")
    else:
        flash("Водія с таким id не знайдено", "error")

    return render_template("driver.html", driver_obj=driver_obj)

# @views.route("/<string:name>")
# def greeting(name: str):
#     return f"<h1>Hello {name.capitalize()}!<h1>"
