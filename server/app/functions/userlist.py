from app.functions.webscraper import webscrape
from app.other import day_dict
from app.tables import UserModel

from datetime import date
from flask_jwt_extended import get_jwt_identity, jwt_required
import json
import requests


def list_today(user_id):
    today = date.today()
    week = date(today.year, today.month, today.day).strftime("%V")

    with open("server/weekly.json", "r") as f:
        json_object = json.load(f)

    if "week" not in json_object or json_object["week"] != str(week):
        webscrape(week)

    result = get_airing(user_id, today)

    return result


def get_airing(user_id, today):
    result = {"result": []}
    user = UserModel.query.filter_by(id=user_id).first()
    day = day_dict[today.weekday()]

    with open("server/weekly.json", "r") as f:
        json_object = json.load(f)
        for show in user.watching:
            show_id = show.show_id
            show_title = show.show_title
            if show_id in json_object["weekly"]:
                airing_day = json_object["weekly"][show_id]["airing_day"]
                if airing_day == str(day):
                    result["result"].append([show_title, show_id])

    return result


def list_watchlist(user_id):
    user = UserModel.query.filter_by(id=user_id).first()
    result = {"data": []}
    for show in user.watching:
        result["data"].append((f"{show.show_title}", f"{show.show_id}"))

    return result


def get_season():
    today = date.today()
    now = (today.month, today.day)
    if (3, 21) <= now < (6, 21):
        season = "spring"
    elif (6, 21) <= now < (9, 21):
        season = "summer"
    elif (9, 21) <= now < (12, 21):
        season = "fall"
    else:
        season = "winter"

    return season


def list_all():
    today = date.today()
    week = date(today.year, today.month, today.day).strftime("%V")

    with open("server/season.json", "r") as f:
        json_object = json.load(f)

    if "week" not in json_object or json_object["week"] != str(week):
        get_season_anime(week)

    with open("server/season.json", "r") as f:
        json_object = json.load(f)
        return json_object["anime"]


def get_season_anime(week):
    result = {"week": week, "anime": []}

    page = 1
    season_anime = "start"
    while season_anime == "start" or season_anime["pagination"]["has_next_page"]:
        season_anime = requests.get(
            f"https://api.jikan.moe/v4/seasons/now?page={page}&filter=tv"
        ).json()

        for anime in season_anime["data"]:
            result["anime"].append(
                [
                    f"{anime["titles"][0]["title"]}",
                    f"{anime["mal_id"]}",
                ]
            )

        page += 1

    with open("server/season.json", "w") as f:
        weekly_object = json.dumps(result)
        f.write(weekly_object)

    return result


def user(user_id):
    user = UserModel.query.filter_by(id=user_id).first()
    return user.username
