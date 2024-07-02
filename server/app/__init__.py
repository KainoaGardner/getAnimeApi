from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_jwt_extended import JWTManager
from datetime import timedelta

app = Flask(__name__, template_folder="web/templates", static_folder="web/static")
# app = Flask(__name__, template_folder="web/templates")
api = Api(app)
jwt = JWTManager(app)
app.secret_key = "4e1243bd22c66e76c2ba9eddc1f91394e57f9f83"
app.config["JWT_SECRET_KEY"] = (
    "87c1b129fbadd7b6e9abc0a9ef7695436d767aece042bec198a97e949fcbe14c"
)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(weeks=1)

app.permanent_session_lifetime = timedelta(weeks=1)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://postgres:root@localhost:5432/get_anime"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)

from app import endpoints
from app.web import routes
