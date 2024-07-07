from flask import flash, session


def check_login():
    if "user" not in session:
        flash("Not logged it")
        return False
    return True


def get_theme():
    if "theme" not in session:
        session["theme"] = "light"

    theme = session["theme"]
    return theme
