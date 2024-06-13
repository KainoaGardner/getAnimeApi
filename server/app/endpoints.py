from flask import request
from flask_restful import Resource, abort

from app import app, db, api
from app.tables import UserModel, ShowModel, WatchingModel


class UserAccount(Resource):
    def get(self):
        test = request.args.get("login")
        return test

    def post(self):  # LOGIN
        if "login" in request.form:
            username = request.form["login"]
            # user = UserModel.query.filter_by(username=username, password=password)
            # if not user:
            #     abort(400, message="Incorrect Information")
            #
            # return {
            #     "user": {
            #         "id": user.id,
            #         "username": user.username,
            #     }
            # }
            #

        return "2"


api.add_resource(UserAccount, "/users/account")
