from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_jwt import JWT
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SECRET_KEY'] = "this is a random key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/CapstoneP' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning

# UPLOAD FOLDER
UPLOAD_FOLDER = "./app/static/uploads"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config.from_object(__name__)
from app import views
