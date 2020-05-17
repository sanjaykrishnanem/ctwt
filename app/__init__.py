# app/__init__.py
import os
from flask import Flask, render_template, abort, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)
app.config.from_pyfile('config.py')   

Bootstrap(app)
db.init_app(app)
login_manager.init_app(app)
login_manager.login_message = "You are not authorised to see the page. Please log in"
login_manager.login_view = "auth.login"

migrate = Migrate(app, db)
from app import models

from .admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint, url_prefix='/admin')

from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from .home import home as home_blueprint
app.register_blueprint(home_blueprint)

from .lead import lead as lead_blueprint
app.register_blueprint(lead_blueprint)

@app.before_request
def check_for_maintenance(): 
    if request.path == url_for('home.maintenance'):
        return redirect(url_for('home.maintenance'))

@app.errorhandler(403)
def forbidden(error):
    return render_template('errors/403.html', title='Forbidden'), 403

@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html', title='Page Not Found'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html', title='Server Error'), 500