from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/")
@app.route("/index.html")
def index():
    return render_template("index.html")


@app.route("/login.html")
def login():
    return render_template("login.html")


@app.route("/faqs.html")
def faqs():
    return render_template("faqs.html")


@app.route("/contact-us.html")
def contact_us():
    return render_template("contact-us.html")


@app.route("/privacy-policy.html")
def privacy_policy():
    return render_template("privacy-policy.html")


@app.route("/terms-of-service.html")
def terms_of_service():
    return render_template("terms-of-service.html")


@app.route("/manage.html")
def manage():
    return render_template("manage.html")


@app.route("/owner.html")
def owner():
    return render_template("owner.html")


@app.route("/driver.html")
def driver():
    return render_template("driver.html")


@app.route("/director.html")
def director():
    return render_template("director.html")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
