import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import factory
from transitracker import db


engine = create_engine('postgresql://ttadmin:csci4230@localhost/transitracker_dev')
Session = sessionmaker()

# Create the database connection
@pytest.fixture(scope='module')
def connection():
    connection = engine.connect()
    yield connection
    connection.close()

# Start the database session
@pytest.fixture(scope='function')
def session(connection):
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session
    session.close()
    transaction.rollback()

# Construct the user model
class User:
    def __init__(self, firstName,lastName, email, password, privilege):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password
        self.privilege = privilege

# Build a factor from the user model
class UserFactory(factory.Factory):
    firstName = factory.Faker('name')
    lastName = factory.Faker('lastName')
    email = factory.Faker('email')
    password = factory.Faker('password')
    privilege = factory.Faker(0)

    class Meta:
        model = User

# Map the database props to the user model
class UserModel(db.Model):
    __tablename__ = 'account'

    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(20), nullable = False)
    lastName = db.Column(db.String(20), nullable = False)
    email = db.Column(db.String(120), unique=True, nullable = False)
    password = db.Column(db.String(60), nullable = False)
    privilege = db.Column(db.Integer, nullable = False, default=2)

# Map the sql alchemy props to the user model
class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    id = factory.Sequence(lambda n: '%s' % n)
    firstName = factory.Faker('Dean')
    lastName = factory.Faker('Murray')
    email = factory.Faker('dmurray12@edu')
    password = factory.Faker('password123')
    privilege = factory.Faker(0)

    class Meta:
        model = UserModel

# Begin the database transaction
@pytest.fixture(scope='function')
def session(connection):
    transaction = connection.begin()
    session = Session(bind=connection)
    UserFactory._meta.sqlalchemy_session = session # NB: This line added
    yield session
    session.close()
    transaction.rollback()

# Safely delete the test user from the database
def my_func_to_delete_user(session, user_id):
    session.query(UserModel).filter(UserModel.id == user_id).delete()

# Assert the result is correct
def test_case(session):
    user = UserFactory.create()
    assert session.query(UserModel).one()

    my_func_to_delete_user(session, user.id)

    result = session.query(UserModel).one_or_none()
    assert result is None
