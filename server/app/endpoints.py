from flask import request
from flask_restful import Resource

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


class UserList(Resource):
    def get(self, user_id, type):
        if type == "today":
            return list_today(user_id)

        elif type == "watchlist":
            return list_watchlist(user_id)

        else:
            return list_all()


class UserAddDelete(Resource):
    def post(self, user_id, type):
        add_shows = request.json["shows"]
        return add(user_id, add_shows)

    def delete(self, user_id, type):
        if type == "clear":
            clear(user_id)
        elif type == "delete":
            delete_shows = request.json["shows"]
            return delete(user_id, delete_shows)


api.add_resource(UserAccount, "/users/account")
api.add_resource(UserList, "/users/list/<string:user_id>/<string:type>")
api.add_resource(UserAddDelete, "/users/add/<string:user_id>/<string:type>")
