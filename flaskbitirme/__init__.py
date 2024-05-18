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

# Import models here to ensure they are known to SQLAlchemy
from flaskbitirme.models import *

# Now import the fill_database function and call it
from flaskbitirme.dbScript import fill_database

#with app.app_context():
    #fill_database()

# Import routes at the end to avoid circular imports
from flaskbitirme import routes