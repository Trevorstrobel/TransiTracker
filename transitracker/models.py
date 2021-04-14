#Author:                Trevor Strobel

from transitracker import db, login_manager
from flask_login import UserMixin


#session manager
@login_manager.user_loader
def loadUser(user_id):
    return User.query.get(int(user_id))


#User table with support for sessions
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(20), nullable = False)
    lastName = db.Column(db.String(20), nullable = False)
    email = db.Column(db.String(120), unique=True, nullable = False)
    phone = db.Column(db.String(10)) #is this necessary for our users?
    password = db.Column(db.String(60), nullable = False)

    def __repr__(self):
        return f"User('{self.firstName}','{self.lastName}','{self.email}')"


