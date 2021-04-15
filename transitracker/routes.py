#Author:                Trevor Strobel

from flask import request, render_template, flash, redirect, url_for
from transitracker import app, db, bcrypt
from transitracker.forms import CreateAccountForm, LoginForm
from transitracker.models import User
from flask_login import login_user,  logout_user, current_user


#default page
@app.route("/", methods=["GET", "POST"])
#Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    #redirect when logged in
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()


    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() #grabs first entry with that email

        #if the user exists and the password matches the hashed password in the db
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('dashboard'))
        else:
            flash('Login attempt unsuccessful. Check Email and Password', 'danger')





            
    return render_template('login.html', title='Login', form = form)


#Create Account Page
@app.route("/createAccount", methods=["GET", "POST"])
def createAccount():
    #redirect when logged in
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = CreateAccountForm()
    if form.validate_on_submit():
        #hash the password from the form to store in the db
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = User(firstName=form.firstName.data, lastName=form.lastName.data, email=form.email.data, password = hashed_password)

        db.session.add(user)
        db.session.commit()

        #flash a message on successful create
        flash(f'Account Created for {form.firstName.data} {form.lastName.data}. You may now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('create_account.html', title='Create Account', form = form)



#Log out user
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))



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