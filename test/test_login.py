from flask import request, render_template, flash, redirect, url_for
from flask_login import login_user,  logout_user, current_user, login_required
import unittest



def test_login_page_loads(self):
    response = self.client.ge5('/login')
    self.assertIn(b, 'Please Login', response.data)

def login(self):
    response = self.client.get('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


def test_correct_login(self):
    response = self.client.post(
        '/login'
    )