from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from app import api
from app.functions.userlogin import *
from app.functions.userlist import *
from app.functions.useradddelete import *


class UserAccount(Resource):
    def post(self):
        if "login" in request.json:
            username = request.json["login"]["username"]
            password = request.json["login"]["password"]

            return login(username, password)

        elif "register" in request.json:
            username = request.json["register"]["username"]
            password = request.json["register"]["password"]

            return register(username, password)

    def delete(self):
        username = request.json["delete"]["username"]
        password = request.json["delete"]["password"]
        return delete_user(username, password)


class UserListToken(Resource):
    @jwt_required()
    def get(self, type):
        user_id = get_jwt_identity()
        if type == "today":
            return list_today(user_id)

        elif type == "watchlist":
            return list_watchlist(user_id)
        elif type == "user":
            return user(user_id)
        else:
            return 404


class UserList(Resource):
    def get(self):
        return list_all()


class UserAddDelete(Resource):
    @jwt_required()
    def post(self, type):
        user_id = get_jwt_identity()
        add_shows = request.json["shows"]
        return add(user_id, add_shows)

    @jwt_required()
    def delete(self, type):
        user_id = get_jwt_identity()
        if type == "clear":
            clear(user_id)
        elif type == "delete":
            delete_shows = request.json["shows"]
            return delete(user_id, delete_shows)


api.add_resource(UserAccount, "/api/users/account")
api.add_resource(UserListToken, "/api/users/list/token/<string:type>")
api.add_resource(UserList, "/api/users/list/")
api.add_resource(UserAddDelete, "/api/users/add/<string:type>")
