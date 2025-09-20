from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from os import path
from secrets import token_hex
import logging
from Classes.CConfig import config

from db import userDb

if(__name__ == "__main__"):
    app:Flask = Flask(import_name="app")
    app.logger.setLevel(logging.INFO)
    app.config["SECRET_KEY"] = token_hex(16)
    cors = CORS(app) # autoriser le cors pour toutes les routes
    swagger = Swagger(app)

    # registering controllers
    from Controllers.ApiUser import UserBP
    from Controllers.ApiDashBoard import DashBoardBP
    app.register_blueprint(DashBoardBP)
    app.register_blueprint(UserBP)

    # Database Parameters
    param_bdd = f"postgresql+pg8000://{config.PostgresUsername}:{config.PostgresPassword}@{config.PostgresServer}/userDb"
    app.config['SQLALCHEMY_DATABASE_URI'] = param_bdd
    # Creating database instance
    userDb.init_app(app)

    from Models.User import User
    with app.app_context():
        from base import Base
        Base.metadata.create_all(userDb.engine)

    @app.get("/")
    def root(): 
        return app.redirect("/apidocs")
    
    app.run(host='0.0.0.0', port=4999)