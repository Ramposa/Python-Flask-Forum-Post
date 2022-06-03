from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask import Flask, render_template

db = SQLAlchemy()
forumDB = "forumDB.db" # database name


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "b'\xf9_gVA\xcf\x02\rI]\x93\xb0\x83\xc1\xfc\xd9r\xf8\xbb\x08m\xfe\xfa5'" # Secret Key
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{forumDB}' # database location
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Post, Comment, Like

    create_database(app)
    
    @app.errorhandler(404) # https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages/
    def not_found(e):
        return render_template('404.html'), 404

    loginManager = LoginManager()
    loginManager.login_view = "auth.login"
    loginManager.init_app(app)

    @loginManager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists("website/" + forumDB):
        db.create_all(app=app)
        print("Created database!")
