import os

from flask            import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login      import LoginManager
from flask_bcrypt     import Bcrypt
from flask_mail       import Mail
from flask_wtf.csrf   import CSRFProtect
from dotenv import load_dotenv


# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))
env_path = os.path.join(basedir, '../.env')
load_dotenv(dotenv_path=env_path)
app = Flask(__name__)

#csrf initialization
csrf = CSRFProtect(app) 
csrf.init_app(app)

app.config.from_object('app.configuration.Config')

# db = SQLAlchemy  (app) # flask-sqlalchemy
bc = Bcrypt      (app) # flask-bcrypt

lm = LoginManager(   ) # flask-loginmanager
lm.init_app(app) # init the login manager

# app.config['MAIL_SERVER'] = str(os.getenv('MAIL_SERVER'))
# app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
# app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
# app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL')
# app.config['MAIL_USERNAME'] = str(os.getenv('MAIL_USERNAME'))
# app.config['MAIL_PASSWORD'] = str(os.getenv('MAIL_PASSWORD'))


app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = "tsherisherpa@gmail.com"
app.config['MAIL_PASSWORD'] = "ggmaikkfsdjf123"

mail= Mail(app)

db  = SQLAlchemy (app)

# Setup database
@app.before_first_request
def initialize_database():
    db.create_all()

# Import routing, models and Start the App
from app import views, models

print('going well')