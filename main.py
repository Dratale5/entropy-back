from flask import Flask

if(__name__ == "__main__"):
    app:Flask = Flask(import_name="app")

    @app.get("/")
    def root(): 
        return "ok"
    
    app.run(host='0.0.0.0', port=5000)