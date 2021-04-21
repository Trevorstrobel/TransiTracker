#Author:                Trevor Strobel
#Date:                  4/14/2021

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager
import email_validator



#create a Flask instance
app = Flask(__name__) 

#app configs
app.config['SECRET_KEY'] = '22ed86cf8f09a5e907b70d9ee2013502'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ttadmin:csci4230@localhost/transitracker_dev'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#create an instance of the database object
db = SQLAlchemy(app)

#Password encryption
bcrypt = Bcrypt(app) 

#login session manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'





from transitracker import routes