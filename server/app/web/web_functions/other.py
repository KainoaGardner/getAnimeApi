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


def sort_list(anime_list, sort):
    if sort == "name":
        anime_list.sort(key=lambda x: x[1])
    elif sort == "id":
        anime_list.sort(key=lambda x: x[0])
    else:
        anime_list.reverse()

    sorted_list = anime_list

    return sorted_list
