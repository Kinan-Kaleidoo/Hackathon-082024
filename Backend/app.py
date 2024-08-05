from flask import Flask
from flask_login import LoginManager
from urls import configure_routes
from bson import ObjectId
from db import users_collection, user_from_dict
import os
from dotenv import load_dotenv

import warnings
warnings.filterwarnings('ignore')

load_dotenv()

app = Flask(__name__)

# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.secret_key = 'dodo'

configure_routes(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to the login view if not authenticated
login_manager.login_message = "צריכים להיות מחוברים כדי לגשת לדף זה"
mongo_username = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')


@login_manager.user_loader
def load_user(user_id):
    user_data = users_collection.find_one({"_id": ObjectId(user_id)})
    if user_data:
        return user_from_dict(user_data)
    return None


if __name__ == '__main__':
    app.run(debug=True)
