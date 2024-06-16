from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from datetime import timedelta

app = Flask(__name__)
api = Api(app)
app.secret_key = "secret"
app.permanent_session_lifetime = timedelta(weeks=7)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://postgres:root@localhost:5432/get_anime"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

auth_token = "UtpetlB5CCl3tG45LMTBKXB6PlrpAm"
mal_auth_token = "UtpetlB5CCl3tG45LMTBKXB6PlrpAm"

db = SQLAlchemy(app)

from app import endpoints
