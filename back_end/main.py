#Author:                Trevor Strobel
#Date:                  4/13/2021

from flask import Flask, request, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 
from forms import CreateAccountForm, LoginForm
import email_validator



#create a Flask instance
app = Flask(__name__) 

#app configs
app.config['SECRET_KEY'] = '22ed86cf8f09a5e907b70d9ee2013502'
app.config['SQLALCHEMY_DATABASE_URI'] = ''


bcrypt = Bcrypt(app)

#bcrypt.generate_password_hash('testing').decode('utf-8')
#bcrypt.check_password_hash(hashed_var, 'thepassword')

@app.route("/")
#Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@ecu.edu' and form.password.data == 'admin':
            flash('You have logged in successfully', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login attempt unsuccessful. Check Email and Password', 'danger')
    return render_template('login.html', title='Login | TransiTracker', form = form)


#Create Account Page
@app.route("/createAccount", methods=["GET", "POST"])
def createAccount():
    form = CreateAccountForm()
    if form.validate_on_submit():
        #flash a message on successful create
        flash(f'Account Created for {form.firstName.data} {form.lastName.data}.', 'success')
        return redirect(url_for('login'))
    return render_template('create_account.html', title='Create Account', form = form)


#Dashboard page
@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')


#Inventory Page
@app.route("/inventory")
def inventory():
    form = LoginForm()
    return render_template('login.html', title='Login | TransiTracker', form = form)

#Transaction Page
@app.route("/transactions")
def transactions():
    form = LoginForm()
    return render_template('login.html', title='Login | TransiTracker', form = form)

#Employees Page
@app.route("/employees")
def employees():
    form = LoginForm()
    return render_template('login.html', title='Login | TransiTracker', form = form)    

if __name__ == '__main__':
    app.run(debug=True)