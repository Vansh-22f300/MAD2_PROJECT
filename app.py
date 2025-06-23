from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import datetime
from passlib.hash import bcrypt

def create_app():
    app = Flask(__name__)
    app.config.from_object('backend.config.LocalConfig')
    return app