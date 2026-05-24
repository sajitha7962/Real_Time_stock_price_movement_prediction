from flask import Blueprint, render_template, request, redirect, session
from models.db import check_user, create_user

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        user = request.form.get("username")
        pwd = request.form.get("password")

        data = check_user(user, pwd)

        if data:
            session["user"] = user   # 🔥 IMPORTANT
            return redirect("/")
        else:
            error = "Invalid username or password"

    return render_template("login.html", error=error)


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = request.form.get("username")
        pwd = request.form.get("password")

        create_user(user, pwd)
        return redirect("/login")

    return render_template("register.html")


@auth.route("/logout")
def logout():
    session.clear()
    return redirect("/login")