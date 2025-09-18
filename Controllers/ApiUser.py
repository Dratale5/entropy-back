import json
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from Classes.Auth import Auth
from Classes.Entropy import Entropy

UserBP = Blueprint("UserBP", "UserBP")

@UserBP.post("/api/connexion")
def connexion():
    """
    Route permettant à un utilisateur inconnu (visiteur) de s'authentifier.
    ---
    tags:
      - Compte Utilisateur
    parameters:
      - in: formData
        name: username
        type: string
        required: true
        description: Nom de l'utilisateur
      - in: formData
        name: password
        type: string
        required: true
        description: Mot de passe de l'utilisateur
    responses:
      200:
        description: Résultat de la tentative de connexion
        schema:
          type: object
          properties:
            statut:
              type: integer
              example: 1
            message:
              type: string
              example: "Connexion réussie"
            token:
              type: string
              example: "c90e2b95eb7ae9f8f8e08f177bf86ecf"
    """
    leJson:dict = {}
    if not request.form:
        return current_app.response_class(status=204, mimetype="application/json")
    
    username = request.form.get("username", None)
    password = request.form.get("password", None)

    if(username in ["",None] or password in ["",None]):
        leJson["statut"] = 0
        leJson["message"] = "Données manquantes."
        return current_app.response_class(response=json.dumps(leJson), status=400, mimetype="application/json")
    
    resultat = Auth.login(username, password)
    if(resultat[0] == False):
        leJson["statut"] = 0
        leJson["message"] = "Données de connexion invalidées."
        return current_app.response_class(response=json.dumps(leJson), status=400, mimetype="application/json")
    
    leJson["statut"] = 1
    leJson["message"] = "Connexion réussie."
    leJson["token"] = resultat[2]
    return current_app.response_class(response=json.dumps(leJson), status=200, mimetype="application/json")

@UserBP.post("/api/deconnexion")
def deconnexion():
    """
    Route permettant à un utilisateur connu de se déconnecter.
    ---
    tags:
      - Compte Utilisateur
    parameters:
      - in: formData
        name: username
        type: string
        required: true
        description: Nom de l'utilisateur
      - in: header
        name: token
        type: string
        required: true
        description: Token de l'utilisateur
    responses:
      200:
        description: Résultat de la tentative de déconnexion
        schema:
          type: object
          properties:
            statut:
              type: integer
              example: 1
            message:
              type: string
              example: "Connexion réussie"
    """
    leJson:dict = {}
    if not request.form:
        return current_app.response_class(status=204, mimetype="application/json")

    username = request.form.get("username", None)
    token = request.headers.get("Authorization", "").split("Bearer ")[-1]

    if(username in ["",None] or token in ["",None]):
        leJson["message"] = "Informations partiellement manquantes."
        leJson["statut"] = 0
        return current_app.response_class(response=json.dumps(leJson), status=200, mimetype="application/json")

    resultat = Auth.logout(username, token)

    if(resultat[0] == False):
        leJson["message"] = "Problème de déconnexion : " + resultat[1]
        leJson["statut"] = 0
        return current_app.response_class(response=json.dumps(leJson), status=200, mimetype="application/json")

    leJson["message"] = "Déconnexion réussie."
    leJson["statut"] = 1
    return current_app.response_class(response=json.dumps(leJson), status=200, mimetype="application/json")

@UserBP.post("/api/verifiertoken")
def verifiertoken():
    """
    Route permettant de vérifier le token d'un utilisateur connu.
    ---
    tags:
      - Compte Utilisateur
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
    if not request.form:
        return current_app.response_class(status=204, mimetype="application/json")

    username = request.form.get("username", None)
    token = request.headers.get("Authorization", "").split("Bearer ")[-1]

    if(username in ["",None] or token in ["",None]):
        leJson["message"] = "Informations partiellement manquantes."
        leJson["statut"] = 0
        return current_app.response_class(response=json.dumps(leJson), status=200, mimetype="application/json")

    resultat = Auth.verifyToken(username, token)

    if(resultat == False):
        leJson["message"] = "Le token est incorrect" 
        leJson["statut"] = 0
        return current_app.response_class(response=json.dumps(leJson), status=200, mimetype="application/json")

    leJson["message"] = "Le token est correct"
    leJson["statut"] = 1
    return current_app.response_class(response=json.dumps(leJson), status=200, mimetype="application/json")

@UserBP.post("/api/creercompte")
def creercompte():
    """
    Route permettant à un utilisateur inconnu (visiteur) de créer son compte.
    ---
    tags:
      - Compte Utilisateur
    parameters:
      - in: formData
        name: username
        type: string
        required: true
        description: Nom de l'utilisateur
      - in: formData
        name: password
        type: string
        required: true
        description: Mot de passe de l'utilisateur
    responses:
      200:
        description: Résultat de la tentative de connexion
        schema:
          type: object
          properties:
            statut:
              type: float
              example: 2.94770277922009
            message:
              type: string
              example: "Compte créé"
            entropy:
                type: integer
                example: 28
    """
    leJson:dict = {}
    if not request.form:
        leJson["message"] = "Informations entièrement manquantes."
        leJson["statut"] = 0
        return current_app.response_class(status=200, mimetype="application/json")
    
    username = request.form.get("username", None)
    password = request.form.get("password", None)

    if(username in ["",None] or password in ["",None]):
        leJson["message"] = "Informations partiellement manquantes."
        leJson["statut"] = 0
        return current_app.response_class(response=json.dumps(leJson), status=200, mimetype="application/json")
    
    resultat = Auth.create_account(username, password)
    
    if(resultat[0] == False):
        leJson["message"] = "Création de compte impossible : " + resultat[1]
        leJson["statut"] = 0
        return current_app.response_class(response=json.dumps(leJson), status=200, mimetype="application/json")
    
    leJson["message"] = "Compte créé"
    leJson["statut"] = 1
    leJson["entropy"] = resultat[2]
    return current_app.response_class(response=json.dumps(leJson), status=200, mimetype="application/json")