#Author:                Trevor Strobel

from flask import request, render_template, flash, redirect, url_for
from transitracker import app, db, bcrypt
from transitracker.forms import CreateAccountForm, LoginForm, EmployeeSearchForm
from transitracker.models import Employee, Item, Transaction, employeeCols
from flask_login import login_user,  logout_user, current_user



#------------------------------Account Routes--------------------------------

#default page
@app.route("/", methods=["GET", "POST"])
#Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    #redirect when logged in
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm() #loads the form from forms.py


    if form.validate_on_submit():
        user = Employee.query.filter_by(email=form.email.data).first() #grabs first entry with that email

        #TODO: Flask throws an error when the wrong password is given instead of just saying "wrong password".
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

    form = CreateAccountForm() #loads the form from forms.py
    if form.validate_on_submit():
        #hash the password from the form to store in the db
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = Employee(firstName=form.firstName.data, lastName=form.lastName.data, email=form.email.data, password = hashed_password)

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




#------------------------------Dashboard Routes--------------------------------
#Dashboard page
@app.route("/dashboard")
    #redirect user if they're not logged in
    if not(current_user.is_authenticated):
        return redirect(url_for('login'))
        
def dashboard():
    #TODO: fetch last 10 transactions and return with render_template
    #TODO: fetch items that need attention from inventory (below or near threshold). return with render_template
   
    return render_template('dashboard.html', title ='Dashboard') # alertInv = alertInventory, recentTrans = recentTransactions)


#------------------------------Inventory Routes--------------------------------
#Inventory Page
@app.route("/inventory")
def inventory():
    #redirect user if they're not logged in
    if not(current_user.is_authenticated):
        return redirect(url_for('login'))

    inventory = Item.query.all()
    return render_template('inventory.html', title='Inventory', data = inventory)

@app.route("/addItem")
def addItem():
    #redirect user if they're not logged in
    if not(current_user.is_authenticated):
        return redirect(url_for('login'))

    #create add item code here.
    return redirect(url_for('inventory'))




#------------------------------Transaction Routes--------------------------------
#Transaction Page
@app.route("/transactions")
def transactions():
    #redirect user if they're not logged in
    if not(current_user.is_authenticated):
        return redirect(url_for('login'))

    transactions = Transaction.query.all()
    return render_template('transactions.html', title='Transactions', data = transactions)


#------------------------------Employee Routes--------------------------------
#Employees Page
@app.route("/employees", methods=["GET", "POST"])
def employees():
    
    #redirect user if they're not logged in
    if not(current_user.is_authenticated):
        return redirect(url_for('login'))


    search = EmployeeSearchForm()
    users = Employee.query.with_entities(Employee.firstName, Employee.lastName, Employee.email).all()
    return render_template('employees.html', title='Employees', column_html = employeeCols, data_html = users, search = search) 