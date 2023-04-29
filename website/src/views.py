from flask import Blueprint, render_template

views = Blueprint("views", __name__)


# page with general access
@views.route("/")
@views.route("/main.html")
def main():
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
def owner():
    return render_template("owner.html")


@views.route("/driver.html")
def driver():
    return render_template("driver.html")


@views.route("/director.html")
def director():
    return render_template("director.html")
