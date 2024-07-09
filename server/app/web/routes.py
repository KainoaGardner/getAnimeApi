from flask import redirect, url_for, render_template, flash, session, request
import requests
import webbrowser

from app import app, db
from app.web.web_functions.other import *
from app.web import APIBASE


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user" in session:
        flash("Already logged in")
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

            flash("Logged in")
            return redirect(url_for("user"))

    theme = get_theme()
    return render_template("login.html", theme=theme)


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out")

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
            flash("Account registered")
            return redirect(url_for("logout"))

    theme = get_theme()

    return render_template("register.html", theme=theme)


@app.route("/delete_user", methods=["GET", "POST"])
def delete_user():
    if not check_login():
        return redirect(url_for("login"))

    if "yes_delete" in request.form:
        username = request.form["username"]
        password = request.form["password"]
        if username != session["user"]["username"]:
            flash("Incorrect Information")
            return redirect(url_for("delete_user"))

        user_response = requests.delete(
            APIBASE + f"users/account",
            json={"delete": {"username": username, "password": password}},
        )
        if user_response.status_code != 404:
            flash("User deleted")
            return redirect(url_for("logout"))
        else:
            flash("Incorrect Information")
            return redirect(url_for("delete_user"))
    elif "no_delete" in request.form:
        return redirect(url_for("user"))

    theme = get_theme()

    return render_template("user_clear.html", theme=theme)


@app.route("/user")
def user():
    if not check_login():
        return redirect(url_for("login"))

    user = session["user"]

    theme = get_theme()

    return render_template("user.html", user=user, theme=theme)


@app.route("/list/all", methods=["GET", "POST"])
def list_all():
    user_response = requests.get(APIBASE + f"users/list").json()
    anime_list = []
    for anime in user_response:
        anime_list.append(
            [anime, user_response[anime]["title"], user_response[anime]["image"]]
        )

    sort_type = "date"
    if request.method == "POST":
        if "name" in request.form:
            sort_type = "name"
        elif "id" in request.form:
            sort_type = "id"
        else:
            sort_type = "recent"
    anime_list = sort_list(anime_list, sort_type)
    theme = get_theme()
    return render_template("lists/list_all.html", anime_list=anime_list, theme=theme)


@app.route("/list/watchlist", methods=["GET", "POST"])
def list_watchlist():
    if not check_login():
        return redirect(url_for("login"))

    user = session["user"]
    token = user["token"]
    headersAuth = {"Authorization": "Bearer " + token}

    user_response = requests.get(
        APIBASE + f"users/list/token/watchlist", headers=headersAuth
    ).json()

    anime_list = []
    for anime in user_response:
        anime_list.append(
            [anime, user_response[anime]["title"], user_response[anime]["image"]]
        )

    sort_type = "date"
    if request.method == "POST":
        if "name" in request.form:
            sort_type = "name"
        elif "id" in request.form:
            sort_type = "id"
        else:
            sort_type = "recent"

    anime_list = sort_list(anime_list, sort_type)
    theme = get_theme()
    count = len(user_response)
    return render_template(
        "lists/list_watchlist.html",
        user=user,
        watchlist=anime_list,
        theme=theme,
        count=count,
    )


@app.route("/list/today", methods=["GET", "POST"])
def list_today():
    if not check_login():
        return redirect(url_for("login"))

    user = session["user"]
    token = user["token"]
    headersAuth = {"Authorization": "Bearer " + token}

    user_response = requests.get(
        APIBASE + f"users/list/token/today", headers=headersAuth
    ).json()

    anime_list = []
    for anime in user_response:
        anime_list.append(
            [
                anime,
                user_response[anime]["title"],
                user_response[anime]["image"],
                user_response[anime]["ep_count"],
            ]
        )

    sort_type = "date"
    if request.method == "POST":
        if "name" in request.form:
            sort_type = "name"
        elif "id" in request.form:
            sort_type = "id"
        else:
            sort_type = "recent"
    anime_list = sort_list(anime_list, sort_type)

    theme = get_theme()

    count = len(user_response)
    return render_template(
        "lists/list_today.html",
        user=user,
        airing_list=anime_list,
        theme=theme,
        count=count,
    )


@app.route("/list/add/<id>", methods=["POST"])
def add(id):
    if not check_login():
        return redirect(url_for("login"))

    user = session["user"]
    token = user["token"]
    headersAuth = {"Authorization": "Bearer " + token}

    user_response = requests.post(
        APIBASE + f"users/add/add",
        json={"shows": [id]},
        headers=headersAuth,
    ).json()
    for anime in user_response:
        flash(f"{anime} added")

    return redirect(request.referrer)


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
    for anime in user_response:
        flash(f"{anime} added")

    return redirect(request.referrer)


@app.route("/list/delete/<id>", methods=["POST"])
def delete(id):
    if not check_login():
        return redirect(url_for("login"))

    user = session["user"]
    token = user["token"]
    headersAuth = {"Authorization": "Bearer " + token}

    user_response = requests.delete(
        APIBASE + f"users/add/delete",
        json={"shows": [id]},
        headers=headersAuth,
    ).json()
    for anime in user_response:
        flash(f"{anime} deleted")

    return redirect(request.referrer)


@app.route("/list/clear", methods=["GET", "POST"])
def clear():
    if not check_login():
        return redirect(url_for("login"))

    user = session["user"]
    token = user["token"]
    headersAuth = {"Authorization": "Bearer " + token}

    if "yes_clear" in request.form:

        user_response = requests.delete(
            APIBASE + f"users/add/clear", headers=headersAuth
        ).json()
        flash("Watchlist cleared")

        return redirect(url_for("list_watchlist"))

    elif "no_clear" in request.form:
        return redirect(url_for("list_watchlist"))
    if "theme" not in session:
        session["theme"] = "light"
    theme = session["theme"]

    return render_template("lists/list_clear.html", theme=theme)


@app.route("/list/nyaa")
def nyaa():
    if not check_login():
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

    return redirect(request.referrer)


@app.route("/theme")
def theme():
    if "theme" not in session:
        session["theme"] = "light"
    if session["theme"] == "dark":
        session["theme"] = "light"
    else:
        session["theme"] = "dark"

    return redirect(request.referrer)
