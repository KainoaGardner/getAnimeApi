from flask import request
from flask_restful import Resource, abort

from app import app, db, api
from app.tables import UserModel, ShowModel, WatchingModel


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


api.add_resource(UserAccount, "/users/account")
