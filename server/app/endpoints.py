from flask import request
from flask_restful import Resource, abort
import requests
import json
from datetime import date

from app import app, db, api, auth_token, mal_auth_token
from app.tables import UserModel, WatchingModel


class UserAccount(Resource):
    def post(self):
        if "login" in request.json:
            username = request.json["login"]["username"]
            password = request.json["login"]["password"]
            user = UserModel.query.filter_by(
                username=username, password=password
            ).first()
            if user:
                return {"result": f"Logged into {username}"}, 200
            else:
                return {"result": f"User {username} not found"}, 404
        elif "logout" in request.json:
            pass
        elif "register" in request.json:
            username = request.json["register"]["username"]
            password = request.json["register"]["password"]

            exists = UserModel.query.filter_by(username=username).scalar() is not None

            if exists:
                return {"result": f"Username {username} already taken"}, 404
            else:
                user = UserModel(username=username, password=password)
                db.session.add(user)
                db.session.commit()

                return {"result": f"{username} has been register"}, 200


class UserList(Resource):
    def get(self, username, type):
        if type == "today":
            pass
        elif type == "watchlist":
            user = UserModel.query.filter_by(username=username).first()
            result = {"data": []}
            for show in user.watching:
                result["data"].append((f"{show.show_title}", f"ID: {show.show_id}"))

            return result

        else:
            result = {"anime": []}
            page = 1
            season_anime = "start"

            while (
                season_anime == "start"
                or season_anime.json()["pagination"]["has_next_page"]
            ):
                season_anime = requests.get(
                    f"https://api.jikan.moe/v4/seasons/now?page={page}&filter=tv"
                )

                for anime in season_anime.json()["data"]:
                    result["anime"].append(
                        (
                            f"{anime["titles"][0]["title"]}",
                            f"ID: {anime["mal_id"]}",
                        )
                    )

                page += 1

            return result, 200


class UserAddDelete(Resource):
    def post(self, username, type):
        add_shows = request.json["shows"]
        user = UserModel.query.filter_by(username=username).first()
        added = {"added": []}
        for anime_id in add_shows:
            anime = requests.get(
                f"https://api.jikan.moe/v4/anime/{anime_id}/full"
            ).json()
            if "data" in anime:
                title = anime["data"]["titles"][0]["title"]
                exists = (
                    WatchingModel.query.filter_by(
                        show_id=anime_id, user_id=user.id
                    ).first()
                    is not None
                )
                if not exists:
                    anime_model = WatchingModel(show_id=anime_id, show_title=title)
                    user.watching.append(anime_model)
                    db.session.add(anime_model)
                    added["added"].append((title, anime_id))
        db.session.commit()

        return added

    def delete(self, username, type):
        if type == "clear":
            user = UserModel.query.filter_by(username=username).first()
            user.watching = []
            db.session.commit()
        elif type == "delete":
            delete_shows = request.json["shows"]
            deleted = {"deleted": []}
            user = UserModel.query.filter_by(username=username).first()

            for show in delete_shows:
                exists = (
                    WatchingModel.query.filter_by(show_id=show, user_id=user.id).first()
                    is not None
                )

                if exists:
                    anime = WatchingModel.query.filter_by(
                        show_id=show, user_id=user.id
                    ).first()

                    deleted["deleted"].append((anime.show_title, anime.show_id))
                    db.session.delete(anime)

            db.session.commit()
            return deleted


api.add_resource(UserAccount, "/users/account")
api.add_resource(UserList, "/users/list/<string:username>/<string:type>")
api.add_resource(UserAddDelete, "/users/add/<string:username>/<string:type>")
