import yaml
from flask import Flask

class Config:
    def __init__(self, app:Flask):
        # Reading config file
        with open("./Config/config.yaml", "r") as fichierConfig:
           
            config = yaml.load(fichierConfig, Loader=yaml.FullLoader)

            dbConfig = dict(config.get("databases", {}))

            PostgresConfig = dict(dbConfig.get("Postgres", {}))
            self.PostgresServer = PostgresConfig.get("server", "")
            self.PostgresUsername = PostgresConfig.get("username", "")
            self.PostgresPassword = PostgresConfig.get("password", "")


            fichierConfig.close()