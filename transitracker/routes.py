#Author:                Trevor Strobel

from flask import request, render_template, flash, redirect, url_for
from transitracker import app, db, bcrypt
from transitracker.forms import *
from transitracker.models import Employee, Item, Transaction, employeeCols, itemCols, transactionCols
from flask_login import login_user,  logout_user, current_user, login_required
from datetime import date



#creates tables if they're not already there.

from transitracker import db
try:
    db.create_all()
    print("Tables created successfully.")
except:
    print("Table creation failed.")



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
        if user and bcrypt.check_password_hash(user.password, form.password.data.encode('utf-8')):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('dashboard'))
        else:
            flash('Login attempt unsuccessful. Check Email and Password', 'danger')

    return render_template('login.html', title='Login', form = form)


#Create Account Page
@app.route("/createAccount", methods=["GET", "POST"])
def createAccount():

    form = CreateAccountForm() #loads the form from forms.py
    if form.validate_on_submit():
        #hash the password from the form to store in the db
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        if Employee.query.first() is None:
            print('first user')
            user = Employee(firstName=form.firstName.data, lastName=form.lastName.data, email=form.email.data, password = hashed_password, privilege=1)
        else:
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
@login_required
def dashboard():

    cur = current_user
    name = cur.firstName

    #TODO: fetch items that need attention from inventory (below or near threshold). return with render_template

    # Here we retrieve the inventory. 
    inventory = Item.query.with_entities(Item.name, Item.inStock, Item.threshold, Item.vendorName, Item.vendorURL).all()

    #alertInv will hold the items that need to be brought to the users attention,
    # that is, items whose stock is lower than the reorder threshold or items whose
    # stock is nearing the threshold.
    alertInv = []


    for item in inventory: 
        difference = item.inStock - item.threshold # used to determine if an item will need reordering soon
        twentyP = item.threshold * 0.2 # represents 20% of the minimum required stock. 

        #add items whos stock is below the threshold
        if item.inStock <= item.threshold:
            alertInv.append(item) 
            inventory.remove(item) #remove the item from the local inventory list to prevent dupes.

        #add items whose stock is less than 20% of the threshold above the threshold. (will need to be reordered soon.)    
        elif (difference > 0 and difference <= twentyP):
            alertInv.append(item)
            inventory.remove(item) #remove the item from the local inventory list to prevent dupes.


    #Fetch all the transactions
#     transactions = Transaction.query.with_entities(Transaction.employee_id, Transaction.item_id, Transaction.num_taken, Transaction.count_before, Transaction.date)
#     transactions = transactions.order_by(Transaction.id.desc()) #puts all transactions in order from most recent-oldest
#     trans = []
#     tentran = [] #holds the 10 most recent transactions
#     for t in transactions:  #adds the users name to the transaction and replaces the employee_id
#         emp_id = t[0]
#         i_id = t[1]
#         user = Employee.query.filter_by(id=emp_id).first() #grabs first entry with that email
#         item = Item.query.filter_by(id=i_id).first()
#
#         if(user != None and item != None ): #checks to see if there are any transactions present in the return from the db.
#
#             trans.append(((user.firstName + " " + user.lastName), item.name, t.num_taken, t.count_before, t.date))
#
#             count = 0
#             #adds the 10 most recent transactions to the top 10 list.
#             for i in range(len(trans)):
#                 if count <= 10:
#                     tentran.append(trans[count])
#                     count += 1
#         elif(user == None):
#             print("user is None")



    #Grabs all transactions and puts them in descending order where most recent is at the top
    transactions = Transaction.query.with_entities(Transaction.id, Transaction.employee_id, Transaction.item_id, Transaction.num_taken, Transaction.count_before, Transaction.date)
    transactions = transactions.order_by(Transaction.id.desc())
    trans = [] #Holds transactions with first and last name in replace of employee id
    for t in transactions:  #Changes employee id to the employees first and last name for transaction
        emp_id = t[1]
        i_id = t[2]
        user = Employee.query.filter_by(id=emp_id).first() #grabs first entry with that email
        item = Item.query.filter_by(id=i_id).first()
        trans.append(((user.firstName + " " + user.lastName), item.name, t.num_taken, t.count_before, t.date))
    tentran = []    #holds the 10 most recent transactions
    count = 0
    for item in trans:  #Goes through transactions and puts the most recent ten into the tentran list
        count += 1
        if count == 11:
            break
        else:
            tentran.append(item)





    return render_template('dashboard.html', title ='Dashboard', inv_data_html =alertInv, inv_column_html = itemCols, trans_column_html = transactionCols, trans_data_html = tentran, name= name) # alertInv = alertInventory, recentTrans = recentTransactions)


#------------------------------Inventory Routes--------------------------------
#Inventory Page
@app.route("/inventory")
@login_required
def inventory():
 
    inventory = Item.query.with_entities(Item.id, Item.name, Item.inStock, Item.threshold, Item.vendorName, Item.vendorURL).all()
    return render_template('inventory.html', title='Inventory', column_html=itemCols,  data_html = inventory)

@app.route("/createItem", methods=['GET', 'POST'])
def createItem():
    #redirect user if they're not logged in
    if not(current_user.is_authenticated):
        return redirect(url_for('login'))
    #load form
    form = CreateItemForm()

    if form.validate_on_submit():
        #submit the data to the database
        #create item object that represents a row in the Item table. 
        item = Item(name=form.name.data, inStock=form.inStock.data, 
                    threshold=form.threshold.data, vendorName=form.vendorName.data, 
                    vendorURL=form.vendorURL.data)

        #add and commit the new item object.
        db.session.add(item)
        db.session.commit()

        #flash a message on successful create
        flash(f'Item  {form.name.data} created. ', 'success')
        return redirect(url_for('inventory'))
    


    return render_template('create_item.html', title='Create Item', form = form)


@app.route("/editItem/<int:item_id>", methods=['GET', 'POST'])
def editItem(item_id):
    item = Item.query.get_or_404(item_id) #returns 404 if item doesnt exist.
    
    #create form object 
    form = EditItemForm()

    

    #if the user submits changes, update the DB.
    if form.validate_on_submit():
        item.name = form.name.data
        item.inStock = form.inStock.data
        item.threshold = form.threshold.data
        item.vendorName = form.vendorName.data
        item.vendorURL = form.vendorURL.data

        #commit to databse
        db.session.commit()
        flash('The item has been updated', 'success')
        return redirect(url_for('inventory'))

    elif request.method == 'GET': #populates fields on the page on 'GET' method
        form.name.data = item.name
        form.inStock.data = item.inStock
        form.threshold.data = item.threshold
        form.vendorName.data = item.vendorName
        form.vendorURL.data = item.vendorURL
    
    priv = False
    if current_user.privilege == 1:
        priv = True

    return render_template('edit_item.html', title=item.name, item=item, form=form, priv=priv)

#------------------------------Transaction Routes--------------------------------
#Transaction Page
@app.route("/transactions", methods=['GET', 'POST'])
@login_required
def transactions():
    #Grabs all transactions
    transactions = Transaction.query.with_entities(Transaction.id, Transaction.employee_id, Transaction.item_id, Transaction.num_taken, Transaction.count_before, Transaction.date)
    #Puts transactions in order from most recent to the oldest
    transactions = transactions.order_by(Transaction.id.desc())
    #Querys the transactions from search parameters
    searchTransactions = Transaction.query.with_entities(Transaction.employee_id, Transaction.item_id, Transaction.date).all()

    trans = [] #holds all transactions with first and last name in place of employee_id
    i = 0
    for t in transactions:
        print(t)
        emp_id = t[1]
        i_id = t[2]
        user = Employee.query.filter_by(id=emp_id).first() #grabs first entry with that email
        item = Item.query.filter_by(id=i_id).first()
        trans.append((t.id, (user.firstName + " " + user.lastName), item.name, t.num_taken, t.count_before, t.date))

    search = TransactionSearchForm()
    searchData = []
    if search.validate_on_submit(): #check for form validation (in this case, just need any input)
        if search.searchBtn.data:
            #gets the information from the search bar
            param = search.searchStr.data
            #Goes through the transactions to see if the search information is in a transaction
            for t in trans:
                for entry in t:
                    if entry == param:
                        searchData.append(t)

    x = len(searchData)
    if x != 0:
        trans = searchData


    return render_template('transactions.html', title='Transactions', data_html = trans, column_html = transactionCols, employees_html = employees, search = search)



#Take Item route
@app.route("/takeItem", methods=['GET', 'POST'])
def takeItem():

    form = CreateTransactionForm()

    if form.validate_on_submit():
        #Grab the item from the item ID
        inventory = Item.query.with_entities(Item.id, Item.name, Item.inStock, Item.threshold, Item.vendorName, Item.vendorURL).all()
        for inv in inventory: #Loops through the inventory to see if the search parameter is in the inventory
            for value in inv:
                if form.name.data == inv[1]:    #Checks to see if item is in inventory
                    item = Item.query.with_entities(Item.name, Item.inStock).first()
                    item = Item.query.filter_by(name=form.name.data).first() #grabs first entry with that email
                    employee = Employee.query.with_entities(Employee.id).first()


                    today = date.today() #gets the date of the transaction
                    d1 = today.strftime("%m/%d/%Y")
                    #Remove the number taken from the database
                    item.inStock = item.inStock - form.num_taken.data
                    tran = Transaction(employee_id = current_user.id, item_id = item.id, num_taken = form.num_taken.data, count_before = item.inStock, date= d1)

                    db.session.add(tran)
                    db.session.commit()
                    flash('The transaction has been made', 'success')
                    return redirect(url_for('transactions'))
                    break
        flash('Could not find item in inventory.', 'danger') #Alerts user if item was not found
        return redirect(url_for('transactions'))

    return render_template('create_transaction.html', title='Create Transaction', form = form)


#------------------------------Employee Routes--------------------------------
#Employees Page
@app.route("/employees", methods=["GET", "POST"])
@login_required
def employees():
    

    #define the search form
    search = EmployeeSearchForm()
    #Define Default search params (All employees)
    users = Employee.query.with_entities(Employee.id, Employee.firstName, Employee.lastName, Employee.email).all()
    searchResults = []
    #if the user submits a search, search the db for users with first or last name that matches.
    if search.validate_on_submit(): #check for form validation (in this case, just need any input)
        if search.searchBtn.data:  # if the searchBtn is pressed...
            param = search.searchStr.data
            for acct in users:
                print(acct)
                for value in acct:  #goes through each of the employeeCols and searches to see if param is equal to the employee information
                    print(value)
                    x = acct[1] + " " + acct[2]
                    print(x)
                    if param == x:
                        searchResults.append(acct)
                        break
                    elif param == value:
                        searchResults.append(acct)

    x = len(searchResults)
    if x != 0:
        users = searchResults


            
    priv = False #default privilege value
    
    if current_user.privilege == 1:
        priv = True

    
    return render_template('employees.html', title='Employees', 
                    column_html = employeeCols, data_html = users, 
                    search = search, priv= priv, id=current_user.id) 

#Employee Edit Page
@app.route("/editEmployee/<int:user_id>", methods=["GET", "POST"])
@login_required
def editEmployee(user_id):

    print(current_user.id)
    user = Employee.query.get_or_404(user_id) #returns 404 if the user does not exist.
    current = False #determines whether "change password" should be visible (deprecated, but deadlines are short, so im leaving it.)
    form = EditAccountForm() #create form object
    admin = False

    if form.validate_on_submit():
        if form.submit.data:    
            user.firstName = form.firstName.data
            user.lastName = form.lastName.data
            user.email = form.email.data
            
            #sets admin status
            if(form.adminSwitch.data):
                user.privilege = 1
            elif(form.adminSwitch.data == False):
                user.privilege = 2
            

            #commit to db
            db.session.commit()
            flash('Employee account has been updated.', 'success')
            return redirect(url_for('employees'))

        elif form.password.data:
            return redirect(url_for('changePassword', user_id=user_id))

    elif request.method == 'GET': #populates form fields on "GET" method

        form.firstName.data = user.firstName
        form.lastName.data = user.lastName
        form.email.data = user.email

        #sets form data for Admin status
        if(user.privilege == 1):
            form.adminSwitch.data = True
        else:
            form.adminSwitch.data = False

        if current_user.id == user.id or current_user.privilege == 1:
            current = True

        if current_user.privilege == 1:
            admin = True




    return render_template('edit_account.html', title=user.email, user=user, form=form, priv=current, admin=admin) 


# Change Password
@app.route("/changePassword/<int:user_id>", methods=['GET', 'POST'])
@login_required
def changePassword(user_id):
    user = Employee.query.get_or_404(user_id) #returns 404 if the user does not exist.
    form = ChangePasswordForm()

    if form.validate_on_submit(): #if user submits new password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') #hash the new password

        user.password = hashed_password #set hashed password to the user obj's password field

        db.session.commit() #commit the password change
        flash('Changed Password', 'success')
        return redirect(url_for('employees'))
    
    elif request.method == 'GET': #render on a 'GET' 
        return render_template('change_password.html', title="Change Password", user=current_user, form=form)
    