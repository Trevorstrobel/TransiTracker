#Author:                Trevor Strobel

from transitracker import db, login_manager
from flask_login import UserMixin


#session manager
@login_manager.user_loader
def loadUser(employee_id):
    return Employee.query.get(int(employee_id))



#Employee table with support for sessions
#Users with privilege level 2 are 'drivers' as defined in the documenation
class Employee(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(20), nullable = False)
    lastName = db.Column(db.String(20), nullable = False)
    email = db.Column(db.String(120), unique=True, nullable = False)
    password = db.Column(db.String(60), nullable = False)
    privilege = db.Column(db.Integer, nullable = False, default=2)
    transactions = db.relationship('Transaction', backref='employee', lazy = True)


    def __repr__(self):
        return f"Employee('{self.firstName}','{self.lastName}','{self.email}')"

#item table. the main inventory table
class Item(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(40), unique = True, nullable = False)
    inStock = db.Column(db.Integer, nullable = True)
    threshold = db.Column(db.Integer, nullable = True)
    vendorName = db.Column(db.String(500), nullable = True)
    vendorURL = db.Column(db.String(500), nullable = True)
    transactions = db.relationship('Transaction', backref='item', lazy = True)


    def __repr__(self):
        return f"Item('{self.name}','{self.inStock}','{self.threshold}')"

#Transaction table. a Transaction is when a user takes items from the inventory. 
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable = False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable = False)
    num_taken = db.Column(db.Integer, nullable = False)
    count_before = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f"Transaction('{self.employee_id}', '{self.item_id}','{self.num_taken}', '{self.count_before}')"
    


# The following are lists contaiing the column names for various tables.
# This may not be the best place for them, but I'm not sure where else I'd put them.
employeeCols = ['First Name', 'Last Name', 'Email Address']
itemCols = ['Item Name', 'Number In Stock', 'Reorder Threshold', 'Vendor']
transactionCols = ['Employee', 'Item Taken', 'Number Taken', 'Stock Before Transaction']
