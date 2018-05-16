import os

from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
import jwt
from app import db


class User(db.Model):
    """This is a model that defines every user"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    admin = db.Column(db.Boolean, default=False)

    def __init__(self, email, password, admin=False):
        """Initialize a user """
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode('utf-8')
        self.admin = admin

    def is_password_valid(self, password):
        """Compare password with the harsh to check validity"""
        return Bcrypt().check_password_hash(self.password, password)

    def generate_token(self, user_id):
        """Generate an access token required to log in user"""
        try:
            # create a payload to be used in generating token

            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=60),
                'iat': datetime.utcnow(),
                'sub': user_id
            }

            # generate a jwt encoded string
            jwt_string = jwt.encode(
                payload,
                os.environ.get('SECRET'),
                algorithm='HS256'
            )
            return jwt_string
        except Exception as e:
            # import pdb; pdb.set_trace()
            return str(e)

    @staticmethod
    def decode_token(token):
        """A method to decode access token from header"""
        try:
            # decode the token using the SECRET
            payload = jwt.decode(token, os.environ.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # if the token is expired, return an error string
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            return "Invalid token. Please register or login"

    def save(self):
        """Save a user to the database"""
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<User {}>'.format(self.email)


class Order(db.Model):
    """The table for all orders made"""

    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    email = db.Column(db.String(250))
    phone_number = db.Column(db.String(250))
    problem_statement = db.Column(db.String(250))
    leading_channel = db.Column(db.String(250))
    project_type = db.Column(db.String(250))
    preferred_software = db.Column(db.String(500))
    description = db.Column(db.Text)
    done = db.Column(db.Boolean, default=False)
    paid = db.Column(db.Boolean, default=False)

    def __init__(self, name, email, phone_number, problem_statement, leading_channel, project_type, preferred_software,
                 description):
        """Initializing the order"""
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.problem_statement = problem_statement
        self.leading_channel = leading_channel
        self.project_type = project_type
        self.preferred_software = preferred_software
        self.description = description

    def toggle_status(self):
        if not self.done:
            self.done = True
        else:
            self.done = False

    def save(self):
        """Save an order to the database"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete an order from database"""
        db.session.delete(self)
        db.session.commit()
