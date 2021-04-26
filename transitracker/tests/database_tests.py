from flask.ext.testing import TestCase
from transitracker import db


class DatabaseTest(TestCase):

    SQLALCHEMY_DATABASE_URI = "sqlite://transitracker_testing"
    TESTING = True

    def create_app(self):
        # pass in test configuration
        return create_app(self)

    def setUp(self):
        db.create_all()

    def test_add_employee(db_session):
        row = db_session.query(Employee).get(1)
        row.firstName = 'John'
        row.lastName = 'Smith'
        row.email = 'johnsmith@ecu.edu'
        row.password = 'password123'
        row.privilege = False
        assert row.firstName == 'John'
        assert row.lastName == 'Smith'
        assert row.email == 'johnsmith@ecu.edu'
        assert row.password == 'password123'
        assert row.privilege == False

    def test_add_item(db_session):
        row = db_session.query(Item).get(1)
        row.id = 0
        row.name = 'Clock'
        row.inStock = 13
        row.threshold = 14
        row.vendorName = 'transit310'
        row.vendorURL = 'transit310@ecu.edu'
        assert row.id == 0
        assert row.name == 'Clock'
        assert row.inStock == 13
        assert row.threshold == 14
        assert row.vendorName == 'transit310'
        assert row.vendorURL == 'transit310@ecu.edu'

    def tearDown(self):
        db.session.remove()
        db.drop_all()
