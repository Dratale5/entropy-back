from secrets import token_hex
from hashlib import sha512
from flask import current_app, request
import json
from Classes.Entropy import Entropy
from db import userDb
from Classes.CConfig import config
from Models.User import User


class Dash:

    @staticmethod
    def getAllUsers():
        with current_app.app_context():
            return userDb.session.query(User).all()


