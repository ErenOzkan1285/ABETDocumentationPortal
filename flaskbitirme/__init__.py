from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# APP INITIALIZATION
app = Flask(__name__)

app.config['SECRET_KEY'] = '57dfgdfgdhty5'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#from flaskbitirme.models import *
from flaskbitirme import routes
