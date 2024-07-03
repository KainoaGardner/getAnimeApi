from flask import redirect, url_for, render_template, flash, session, request
import requests
import webbrowser
from PIL import Image

from app import app, db
from app.web import APIBASE


@app.route("/home")
def home():
    if "theme" not in session:
        session["theme"] = "light"

    theme = session["theme"]
    return render_template("home.html", theme=theme)


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user" in session:
        return redirect(url_for("user"))
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_response = requests.post(
            APIBASE + "users/account",
            json={"login": {"username": username, "password": password}},
        )
        if user_response.status_code != 404:
            session["user"] = {
                "username": username,
                "token": user_response.json()["token"],
            }

            return redirect(url_for("user"))
    if "theme" not in session:
        session["theme"] = "light"

    theme = session["theme"]
    return render_template("login.html", theme=theme)


@app.route("/logout")
def logout():
    session.pop("user", None)
    if "theme" not in session:
        session["theme"] = "light"

    theme = session["theme"]

    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user_response = requests.post(
            APIBASE + "users/account",
            json={"register": {"username": username, "password": password}},
        )
        if user_response.status_code != 404:
            return redirect(url_for("logout"))

    if "theme" not in session:
        session["theme"] = "light"

    theme = session["theme"]

    return render_template("register.html", theme=theme)


@app.route("/delete_user", methods=["GET", "POST"])
def delete_user():
    if "user" not in session:
        return redirect(url_for("login"))

    if "yes_delete" in request.form:
        username = request.form["username"]
        password = request.form["password"]
        if username != session["user"]["username"]:
            print("test")
            return redirect(url_for("delete_user"))

        user_response = requests.delete(
            APIBASE + f"users/account",
            json={"delete": {"username": username, "password": password}},
        )
        if user_response != 404:
            return redirect(url_for("logout"))
        else:
            return redirect(url_for("user"))
    elif "no_delete" in request.form:
        return redirect(url_for("user"))

    return render_template("user_clear.html")


@app.route("/user")
def user():
    if "user" not in session:
        return redirect(url_for("login"))
    user = session["user"]
    if "theme" not in session:
        session["theme"] = "light"

    theme = session["theme"]

    return render_template("user.html", user=user, theme=theme)


@app.route("/list/all")
def list_all():
    user_response = requests.get(APIBASE + f"users/list").json()
    theme = session["theme"]
    return render_template("lists/list_all.html", anime_list=user_response, theme=theme)


@app.route("/list/watchlist")
def list_watchlist():
    if "user" not in session:
        return redirect(url_for("login"))

    user = session["user"]
    token = user["token"]
    headersAuth = {"Authorization": "Bearer " + token}

    watchlist = requests.get(
        APIBASE + f"users/list/token/watchlist", headers=headersAuth
    ).json()

    if "theme" not in session:
        session["theme"] = "light"
    theme = session["theme"]
    return render_template(
        "lists/list_watchlist.html", user=user, watchlist=watchlist, theme=theme
    )


@app.route("/list/today")
def list_today():
    if "user" not in session:
        return redirect(url_for("login"))
    user = session["user"]
    token = user["token"]
    headersAuth = {"Authorization": "Bearer " + token}

    airing_list = requests.get(
        APIBASE + f"users/list/token/today", headers=headersAuth
    ).json()

    theme = session["theme"]
    return render_template(
        "lists/list_today.html", user=user, airing_list=airing_list, theme=theme
    )


@app.route("/list/add/<id>/<sent_from>", methods=["POST"])
def add(id, sent_from):
    if "user" not in session:

        return redirect(url_for("login"))

    user = session["user"]
    token = user["token"]
    headersAuth = {"Authorization": "Bearer " + token}

    user_response = requests.post(
        APIBASE + f"users/add/add",
        json={"shows": [id]},
        headers=headersAuth,
    ).json()

    if sent_from == "all":
        return_page = "list_all"
    elif sent_from == "watchlist":

        return_page = "list_watchlist"
    else:
        return_page = "other"

    return redirect(url_for(return_page))


@app.route("/list/add/id", methods=["POST"])
def add_id():
    if "user" not in session:
        return redirect(url_for("login"))

    user = session["user"]
    token = user["token"]
    headersAuth = {"Authorization": "Bearer " + token}

    id = request.form["anime_id"]

    user_response = requests.post(
        APIBASE + f"users/add/add",
        json={"shows": [id]},
        headers=headersAuth,
    ).json()

    return redirect(url_for("list_watchlist"))


@app.route("/list/delete/<id>/<sent_from>", methods=["POST"])
def delete(id, sent_from):
    if "user" not in session:
        return redirect(url_for("login"))

    user = session["user"]
    token = user["token"]
    headersAuth = {"Authorization": "Bearer " + token}

    user_response = requests.delete(
        APIBASE + f"users/add/delete",
        json={"shows": [id]},
        headers=headersAuth,
    ).json()

    if sent_from == "watchlist":

        return_page = "list_watchlist"
    else:
        return_page = "list_today"

    return redirect(url_for(return_page))


@app.route("/list/clear", methods=["POST"])
def clear():
    if "user" not in session:
        return redirect(url_for("login"))

    user = session["user"]
    token = user["token"]
    headersAuth = {"Authorization": "Bearer " + token}

    if "yes_clear" in request.form:

        user_response = requests.delete(
            APIBASE + f"users/add/clear", headers=headersAuth
        ).json()

        return redirect(url_for("list_watchlist"))
    elif "no_clear" in request.form:
        return redirect(url_for("list_watchlist"))

    return render_template("lists/list_clear.html")


@app.route("/list/nyaa")
def nyaa():

    if "user" not in session:
        return redirect(url_for("login"))
    user = session["user"]
    token = user["token"]
    headersAuth = {"Authorization": "Bearer " + token}

    airing_list = requests.get(
        APIBASE + f"users/list/token/today", headers=headersAuth
    ).json()
    if airing_list != "bad":
        for anime in airing_list:
            title = airing_list[anime]["title"].lower()
            title = title.replace(" ", "+")
            webbrowser.open(f"https://nyaa.si/?f=0&c=0_0&q={title}&s=id&o=desc")

    return redirect(url_for("list_today"))


@app.route("/theme")
def theme():
    if "theme" not in session:
        session["theme"] = "light"
    if session["theme"] == "dark":
        session["theme"] = "light"
    else:
        session["theme"] = "dark"

    return redirect(url_for("user"))
