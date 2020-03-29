from app            import db, app
from random         import randint
from flask_login    import UserMixin
from itsdangerous   import TimedJSONWebSignatureSerializer  as Serializer

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
    password_reset_token = db.Column(db.String(200))

    def __init__(self, email, password, firstname= "", lastname="", address="", description="", country="", city= "",  phone="", password_reset_token=""):
        self.phone       = phone
        self.password    = password
        self.email       = email
        self.firstname   = firstname
        self.lastname    = lastname
        self.address     = address
        self.description = description
        self.country     = country
        self.city        = city
        self.password_reset_token = password_reset_token

    def __repr__(self):
        return '<User %r - %s>' % (self.id) % (self.email)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    
    @staticmethod
    def get_token(n=6):
        range_start = 10**(n-1)
        range_end = (10**n)-1
        return randint(range_start, range_end)
        
        
