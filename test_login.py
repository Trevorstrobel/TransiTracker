import pytest
from flask import Flask
from transitracker import app, db
from transitracker.models import Employee


def new_employee():
    user = Employee('folu@gmail.com', '1234')
    return user

def test_client():
    flask_app = Flask('__main__')
    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        #Application context
        with flask_app.app_context():
            return testing_client 


# Create the database and the database table
def create_database(test_client):
    db.create_all()
    # Insert user data
    user1 = Employee(firstname = 'Folu', lastname = 'Fatolu', email='folu@gmail.com', password='1234')
    db.session.add(user1)
    # Commit the changes for the users
    db.session.commit()
    return 
    db.drop_all()


def test_login_employee(test_client, email, password):
    return test_client.post('/login',
                     data=dict(email='folu@gmail.com', password='1234'),
                     follow_redirects=True)
    return test_client.get('/logout', follow_redirects=True)


def test_login_page(test_client):
    
    # When the '/login' page is requested (GET), check the response is valid
    
    response = test_client.get('/login')
    assert response.status_code == 200
    assert b'Email' in response.data
    assert b'Password' in response.data


def test_valid_login_logout(test_client, create_database):

  
    # When the '/login' page is posted to (POST), check the response is valid
    
    response = test_client.post('/login',
                                data=dict(email='folu@gmail.com', password='1234'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Welcome folu@gmail.com!' in response.data
    #assert b'Logout' in response.data
    #assert b'Login' not in response.data
