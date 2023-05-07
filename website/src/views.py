import random
from typing import List

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from src.models import DriverDatabase, Driver, User, DirectorDatabase, Director, UserDatabase, OwnerDatabase, Owner

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
    return render_template("faqs.html", current_user=current_user)


@views.route("/contact.html")
def contact():
    return render_template("contact.html", current_user=current_user)


@views.route("/privacy_policy.html")
def privacy_policy():
    return render_template("privacy_policy.html", current_user=current_user)


@views.route("/terms_of_service.html")
def terms_of_service():
    return render_template("terms_of_service.html", current_user=current_user)


@views.route("/about.html")
def about():
    return render_template("about.html", current_user=current_user)


@views.route("/owner.html")
@login_required
def owner():
    if current_user.role_id != 1:
        return redirect(url_for("views.main"))

    directors = DirectorDatabase.get_all_directors()
    directors_urls = [f"director.html?id={d.id}" for d in directors]

    no_role_users = UserDatabase.get_all_no_role_users()
    no_role_users_urls = [f"promotion.html?user_id={u.id}" for u in no_role_users]
    return render_template("owner.html", current_user=current_user, directors=directors, directors_urls=directors_urls,
                           no_role_users=no_role_users, no_role_users_urls=no_role_users_urls)


@views.route("/director.html")
@login_required
def director():
    if current_user.role_id not in [1, 2]:
        return redirect(url_for("views.main"))

    director_obj: Director = None
    drivers: List[Driver] = None
    drivers_urls: List[str] = None
    no_role_users: List[User] = None
    no_role_users_urls: List[str] = None
    take_away_role_url: str = None

    if current_user.role_id == 2:
        director_obj = DirectorDatabase.get_director_by_user_id(current_user.id)
    else:
        # current_user.role_id == 1
        director_id = int(request.args.get("id"))
        director_obj = DirectorDatabase.get_director_by_director_id(director_id)
        director_user_id = DirectorDatabase.get_user_id_by_director_id(director_id)
        take_away_role_url = f"/take_away_role?user_id={director_user_id}"

    drivers: List[Driver] = DirectorDatabase.get_drivers_by_director_id(director_obj.id)
    drivers_urls = [f"driver.html?id={d.id}" for d in drivers]

    no_role_users = UserDatabase.get_all_no_role_users()
    no_role_users_urls = [f"promotion.html?user_id={u.id}" for u in no_role_users]

    return render_template("director.html", director_obj=director_obj, drivers=drivers, drivers_urls=drivers_urls,
                           no_role_users=no_role_users, no_role_users_urls=no_role_users_urls,
                           take_away_role_url=take_away_role_url)


@views.route("/promotion.html")
@login_required
def promotion():
    user_id = request.args.get("user_id")
    if user_id is None or current_user.role_id not in [1, 2]:
        return redirect(url_for("views.main"))

    user_id = int(user_id)
    user_obj = UserDatabase.get_user_by_user_id(user_id)
    grant_driver_role_url = f"/grant_driver_role?user_id={user_id}"
    grant_director_role_url = f"/grant_director_role?user_id={user_id}"
    grant_owner_role_url = f"/grant_owner_role?user_id={user_id}"

    return render_template("promotion.html", user_obj=user_obj, current_user=current_user,
                           grant_driver_role_url=grant_driver_role_url,
                           grant_director_role_url=grant_director_role_url,
                           grant_owner_role_url=grant_owner_role_url)


@views.route("/grant_driver_role")
@login_required
def grant_driver_role():
    # function expects url like that "/grant_driver_role?user_id=-8"

    user_id = request.args.get("user_id")
    if user_id is None or current_user.role_id != 2:
        return redirect(url_for("views.main"))

    user_id = int(user_id)
    user_obj = UserDatabase.get_user_by_user_id(user_id)
    if user_obj.role_id == 4:
        UserDatabase.grant_driver_role_by_user_id(user_id)

        driver_obj = DriverDatabase.get_driver_by_user_id(user_id)
        director_obj = DirectorDatabase.get_director_by_user_id(current_user.id)

        DriverDatabase.set_director_id_by_driver_id(director_id=director_obj.id, driver_id=driver_obj.id)

        # hard code TODO: have to be remade sometime
        route_id = random.choice([-1, 0, 1, 2, 3, 4])
        #

        DriverDatabase.set_route_id_by_driver_id(route_id=route_id, driver_id=driver_obj.id)
    return redirect(url_for("views.main"))


@views.route("/grant_director_role")
@login_required
def grant_director_role():
    # function expects url like that "/grant_director_role?user_id=-8"
    user_id = request.args.get("user_id")
    if user_id is None or current_user.role_id != 1:
        return redirect(url_for("views.main"))

    user_id = int(user_id)
    user_obj = UserDatabase.get_user_by_user_id(user_id)
    if user_obj.role_id == 4:
        UserDatabase.grant_director_role_by_user_id(user_id)
    return redirect(url_for("views.main"))


@views.route("/grant_owner_role")
@login_required
def grant_owner_role():
    # function expects url like that "/grant_owner_role?user_id=-8"
    user_id = request.args.get("user_id")
    if user_id is None or current_user.role_id != 1:
        return redirect(url_for("views.main"))

    user_id = int(user_id)
    user_obj = UserDatabase.get_user_by_user_id(user_id)
    if user_obj.role_id == 4:
        UserDatabase.grant_owner_role_by_user_id(user_id)
    return redirect(url_for("views.main"))


@views.route("/take_away_role")
@login_required
def take_away_role():
    # function expects url like that "/take_away_role?user_id=-8"
    user_id = request.args.get("user_id")
    if user_id is None or current_user.role_id != 1:
        return redirect(url_for("views.main"))

    user_id = int(user_id)
    user_obj = UserDatabase.get_user_by_user_id(user_id)
    if user_obj.role_id != 4:
        UserDatabase.take_away_role_by_user_id(user_id)
    return redirect(url_for("views.main"))


# @views.route("/driver.html?id=<string:driver_id>")
@views.route("/driver.html", methods=["GET", "POST"])
@login_required
def driver():
    if current_user.role_id not in [1, 2, 3]:
        return redirect(url_for("views.main"))

    if request.method == "GET":
        driver_obj: Driver = None
        director_obj: Director = None
        owner_obj: Owner = None
        take_away_role_url: str = None

        if current_user.role_id == 3:
            driver_obj = DriverDatabase.get_driver_by_user_id(current_user.id)

        # director views driver account with url: "/driver.html?id=-3", where id is driver_id
        elif current_user.role_id == 2:
            driver_id = request.args.get("id")
            if driver_id is None:
                flash("Водій не вказаний", "error")
            else:
                driver_id = int(driver_id)

                driver_obj = DriverDatabase.get_driver_by_driver_id(driver_id)
                director_obj = DirectorDatabase.get_director_by_user_id(current_user.id)

        elif current_user.role_id == 1:
            driver_id = request.args.get("id")
            if driver_id is None:
                flash("Водій не вказаний", "error")
            else:
                driver_id = int(driver_id)
                driver_obj = DriverDatabase.get_driver_by_driver_id(driver_id)
                owner_obj = OwnerDatabase.get_owner_by_user_id(current_user.id)
                driver_user_id = DriverDatabase.get_user_id_by_driver_id(driver_obj.id)
                take_away_role_url = f"/take_away_role?user_id={driver_user_id}"

        if driver_obj is not None:

            if current_user.role_id == 2 and driver_obj.director_id != director_obj.id:
                flash("Цей водій не призначений до вас, тому ви не можете переглянути інформацію про нього.", "warning")
                driver_obj = None
                return render_template("driver.html", driver_obj=driver_obj, director_obj=director_obj)

            driver_obj.stations = driver_obj.stations.split(driver_obj.station_delimiter)
            driver_obj.stations = [] if len(driver_obj.stations) == 1 and driver_obj.stations[0] == "" \
                else driver_obj.stations

            if not driver_obj.stations:
                flash("На сьогодні вам не призначено маршрут", "info")
        else:
            flash("Водія с таким id не знайдено", "error")

        return render_template("driver.html", driver_obj=driver_obj, director_obj=director_obj, owner_obj=owner_obj,
                               take_away_role_url=take_away_role_url)
    elif request.method == "POST":
        if current_user.role_id == 3:
            flash("Вам не дозволено вносити зміни", "error")
            return redirect(url_for("views.driver"))

        if current_user.role_id in [1, 2]:
            driver_id = int(request.args.get("id"))
            driver_obj = DriverDatabase.get_driver_by_driver_id(driver_id)

            if current_user.role_id == 2:
                director_obj = DirectorDatabase.get_director_by_user_id(current_user.id)

                if driver_obj.director_id != director_obj.id:
                    flash("Цей водій не призначений до вас, тому ви не можете змінювати інформацію про нього.", "error")
                    driver_obj = None
                    return render_template("driver.html", driver_obj=driver_obj, director_obj=director_obj)

            worked_hours = request.form.get("worked_hours")
            if worked_hours is not None and worked_hours != "":
                try:
                    worked_hours = float(worked_hours)
                except ValueError:
                    flash("Відпрацьовані години введені в неправильному форматі", "error")
                    return redirect(f"driver.html?id={driver_id}")

                DriverDatabase.set_worked_hours_by_driver_id(worked_hours=worked_hours, driver_id=driver_id)

            rest_hours = request.form.get("rest_hours")
            if rest_hours is not None and rest_hours != "":
                try:
                    rest_hours = float(rest_hours)
                except ValueError:
                    flash("Час відпочинку введений в неправильному форматі", "error")
                    return redirect(f"driver.html?id={driver_id}")
                DriverDatabase.set_rest_hours_by_driver_id(rest_hours=rest_hours, driver_id=driver_id)

            return redirect(f"driver.html?id={driver_id}")
