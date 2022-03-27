from flask import Flask
from .models import db,UserModel, CandidateModel
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = 'BadSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///votrbase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False


db.init_app(app) 


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))


from app import views
from .auth import auth  




# blueprint for authentication routes
app.register_blueprint(auth,url_prefix="/auth") 


