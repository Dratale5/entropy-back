import json
from flask import Blueprint, current_app
from Classes.Auth import Auth
from Classes.Entropy import Entropy
from Classes.Dash import Dash
from Classes.CConfig import config


ConfigBP = Blueprint("ConfigBP", "ConfigBP")

@ConfigBP.get("/api/config")
def getConfig():
    """
    Route permettant de récupérer la configuration de l'application.
    ---
    tags:
      - Configuration
    responses:
      200:
        description: Configuration actuelle de l'application
        schema:
          type: object
          properties:
            config:
              type: object
              properties:
                minEntropy:
                  type: integer
                  example: 2
                maxRedundancy:
                  type: integer
                  example: 0.5
            message:
              type: string
              example: "Configuration App"
              description: Message de statut
            statut:
              type: integer
              example: 1
    """
    leJson:dict = {}
    leJson["config"]={}
    leJson["config"]["minEntropy"]=config.MinEntropy
    leJson["config"]["maxRedundancy"]=config.MaxRedondance
    leJson["message"] = "Configuration App"
    leJson["statut"] = 1
    return current_app.response_class(response=json.dumps(leJson), status=200, mimetype="application/json")
