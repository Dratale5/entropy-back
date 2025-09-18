import json
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from Classes.Auth import Auth
from Classes.Entropy import Entropy
from Classes.Dash import Dash

DashBoardBP = Blueprint("DashBoardBP", "DashBoardBP")

@Auth.API_REQUIRES_AUTHENTICATION
@DashBoardBP.post("/api/dashboard/users")
def getAllUsers():
    """
    Route permettant à un utilisateur authentifié de récupérer la liste des utilisateurs.
    ---
    tags:
      - DashBoard
    parameters:
      - in: formData
        name: username
        type: string
        required: true
        description: Nom de l'utilisateur
      - in: header
        name: Authorization
        type: string
        required: true
        description: "Token de l'utilisateur"
    responses:
      200:
        description: Résultat de vérification
        schema:
          type: object
          properties:
            statut:
              type: integer
              example: 1
            message:
              type: string
              example: "Le token est correct"
    """
    leJson:dict = {}
    leJson["Users"] = []
    for user in Dash.getAllUsers():
        leJson["Users"].append({
            "id": user.id,
            "username": user.username
        })

    leJson["message"] = "Liste des Utilisateurs"
    leJson["statut"] = 1
    return current_app.response_class(response=json.dumps(leJson), status=200, mimetype="application/json")
