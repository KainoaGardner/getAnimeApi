from app.tables import UserModel, WatchingModel
from app import db

from datetime import date, datetime
import json
import requests


def add(user_id, add_shows):
    user = UserModel.query.filter_by(id=user_id).first()
    added = {"added": {}}
    for anime_id in add_shows:
        anime = requests.get(f"https://api.jikan.moe/v4/anime/{anime_id}/full").json()
        if "data" in anime:
            title = anime["data"]["titles"][0]["title"]
            image = anime["data"]["images"]["jpg"]["image_url"]
            exists = (
                WatchingModel.query.filter_by(show_id=anime_id, user_id=user.id).first()
                is not None
            )
            if not exists:
                anime_model = WatchingModel(
                    show_id=anime_id, show_title=title, show_image=image
                )
                user.watching.append(anime_model)
                db.session.add(anime_model)
                added["added"].update({anime_id: {"title": title}})

    db.session.commit()

    return added["added"]


def clear(user_id):
    user = UserModel.query.filter_by(id=user_id).first()
    user.watching = []
    db.session.commit()


def delete(user_id, delete_shows):
    deleted = {"deleted": {}}
    user = UserModel.query.filter_by(id=user_id).first()

    for show in delete_shows:
        exists = (
            WatchingModel.query.filter_by(show_id=show, user_id=user.id).first()
            is not None
        )

        if exists:
            anime = WatchingModel.query.filter_by(show_id=show, user_id=user.id).first()

            deleted["deleted"].update({anime.show_id: {"title": anime.show_title}})
            db.session.delete(anime)

    db.session.commit()
    return deleted["deleted"]
