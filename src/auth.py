from flask import Blueprint, render_template, request, flash

from src import cursor

auth = Blueprint("auth", __name__)


# page with general access
@auth.route("/login.html", methods=["GET", "POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    print(request.form)
    return render_template("login.html", boolean=True)


# page with general access
@auth.route("/register.html", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")

        # TODO: add email verification using regexp
        if password != confirm_password:
            flash("Паролі не співпадають. Спробуйте ще.", category="error")
            return render_template("register.html")
        else:
            sql_query = f"""
            insert into trolleybus_site_database.users (user_id, user_email, user_password)
            values (trolleybus_site_database.users_seq.nextval, '{email}', '{password}');
            """
            cursor.execute(sql_query)
            cursor.execute("commit;")

            return render_template("login.html")
    elif request.method == "GET":
        return render_template("register.html")
