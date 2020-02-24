from app         import db
from flask_login import UserMixin

class User(UserMixin, db.Model):

    __tablename__ = 'users'

    id          = db.Column(db.Integer,     primary_key=True)
    email       = db.Column(db.String(120), unique = True)
    phone       = db.Column(db.String(15))
    password    = db.Column(db.String(500))
    firstname   = db.Column(db.String(200))
    lastname    = db.Column(db.String(200))
    address     = db.Column(db.String(200))
    description = db.Column(db.String(200))
    country     = db.Column(db.String(200))
    city        = db.Column(db.String(200))

    def __init__(self, email, password, firstname= "", lastname="", address="", description="", country="", city= "",  phone=""):
        self.phone       = phone
        self.password    = password
        self.email       = email
        self.firstname   = firstname
        self.lastname    = lastname
        self.address     = address
        self.description = description
        self.country     = country
        self.city        = city

    def __repr__(self):
        return '<User %r - %s>' % (self.id) % (self.email)

    def save(self):
        db.session.add(self)
        db.session.commit()
        
        return self
