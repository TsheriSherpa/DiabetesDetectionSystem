""" Configuration File	"""
import os

from dotenv import load_dotenv

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))
env_path = os.path.join(basedir, '../.env')
load_dotenv(dotenv_path=env_path)

class Config():

	CSRF_ENABLED = True
	SECRET_KEY   = os.getenv("SECRET_KEY") 
	
	SQLALCHEMY_TRACK_MODIFICATIONS 	= False
	
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
	# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost:3306/flask_db'
	WTF_CSRF_CHECK_DEFAULT = False