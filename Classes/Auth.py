from secrets import token_hex
from hashlib import sha512
from flask import current_app, request
import json
from Classes.Entropy import Entropy
from db import userDb
from Models.User import User


class Auth:

    @staticmethod
    def login(username:str, password:str) -> tuple[bool,str,str,int]:
        try:
            mdpHash:str = sha512(password.encode("utf-8")).hexdigest()
            with current_app.app_context():
                unUser = userDb.session.query(User).filter(User.username==username,User.passwordHash==mdpHash).first()

                if(unUser == None): return (False, "Identifiants incorrects.", "")

                # New random token
                userToken:str = token_hex(16)

                unUser.token = userToken

                userDb.session.add(unUser)
                userDb.session.commit()
                
                return (True, "Connexion réussie.", userToken, unUser.id)
            
        except Exception as e:
            current_app.logger.error(str(e))
            return (False, "Une erreur est survenue.", "")
        except Exception as e:
            current_app.logger.error(str(e))
            return (False, "Une erreur est survenue.", "")
    


    @staticmethod
    def logout(username:str, userToken:str) -> tuple[bool,str]:
        if(Auth.verifyToken(username, userToken) == False): return  (False, "Action impossible.")

        try:
            with current_app.app_context():
                unUser = userDb.session.query(User).filter(User.username==username,User.token==userToken).first()

                if(unUser == None): return (False, "Action impossible.")

                unUser.token = None

                userDb.session.add(unUser)
                userDb.session.commit()
                
                return (True, "Déconnexion réussie.")
            
        except Exception as e:
            current_app.logger.error(str(e))
            return (False, "Une erreur est survenue.")
        
    

    @staticmethod
    def verifyToken(username:str, userToken:str) -> bool:
        # Controlly the token's validity
        unUser = userDb.session.query(User).filter(User.username==username,User.token==userToken).first()
        if(unUser == None): return False
        else: return True



    @staticmethod
    def create_account(username:str, password:str) -> tuple[bool,str]:
        try:
            mdpHash:str = sha512(password.encode("utf-8")).hexdigest()
            with current_app.app_context():
                unUser = userDb.session.query(User).filter(User.username==username).first()
                if(unUser != None): return (False, "Cet identifiant est déjà utilisé.")

                newUser = User()
                newUser.username = username
                newUser.passwordHash = mdpHash

                userDb.session.add(newUser)
                userDb.session.commit()
                
                return (True, "Compte créé.", Entropy.calculerEntropy(password), Entropy.calculerRedondance(password))
            
        except Exception as e:
            current_app.logger.error(str(e))
            return (False, "Une erreur est survenue.", 0,0)
        except Exception as e:
            current_app.logger.error(str(e))
            return (False, "Une erreur est survenue.", 0,0)
    


    @staticmethod
    def API_REQUIRES_AUTHENTICATION(fonction_origine):
        def wrapper(*args, **kwargs):
            with current_app.app_context():
                
                userId = username = request.headers.get("userId")
                username = request.headers.get("username")
                token = request.headers.get("token")

                unUser = userDb.session.query(User).filter(User.username==username,User.token==token).first()

                if(unUser == None):
                    leJson:dict = {}
                    leJson["statut"] = 0
                    leJson["messages"] = "Token invalide."
                    return current_app.response_class(response=json.dumps(leJson), status=200, mimetype="application/json")

                
            return fonction_origine(*args, **kwargs)
        
        wrapper.__name__ = fonction_origine.__name__
        return wrapper