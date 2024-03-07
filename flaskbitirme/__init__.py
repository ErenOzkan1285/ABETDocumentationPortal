from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# APP INITIALIZATION
app = Flask(__name__)

app.config['SECRET_KEY'] = '57dfgdfgdhty5'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

#from flaskbitirme.models import *
from flaskbitirme import routes
