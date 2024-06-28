from flask import redirect, url_for, render_template, flash, session, request
from app import app, db


@app.route("/home")
def home():
    return render_template("base.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


@app.route("/logout")
def logout():
    return "logout"


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/delete_user")
def delete_user():
    return redirect(url_for("login"))


@app.route("/user")
def user():
    return render_template("user.html")


# @app.route("/list")
# def list():
#     return render_template("list.html")
#


@app.route("/list/all")
def list_all():
    return render_template("lists/list_all.html")


@app.route("/list/watchlist")
def list_watchlist():
    return render_template("lists/list_watchlist.html")


@app.route("/list/today")
def list_today():
    return render_template("lists/list_today.html")


@app.route("/add")
def add():
    return "added"


@app.route("/delete")
def delete():
    return "deleted"


@app.route("/clear")
def clear():
    return "cleared"


@app.route("/nyaa")
def nyaa():
    return "nyaa"
