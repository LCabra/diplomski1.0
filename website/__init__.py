from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy() 
DB_NAME = 'vezbam.db'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] ='beb9f203b24e3db2a29ca4a434073928433e5ab3bdbefdd9a26199c741799ed1'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:zuzuna02@localhost:5432/vezbam'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Pitch

    with app.app_context():
        db.create_all()
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)


    return app

def create_database(app):
    if not path.exists('fajlovi/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')