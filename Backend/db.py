from datetime import datetime
from models import check_password_hash
from models import User
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from flask_login import current_user
import pandas as pd

load_dotenv()
# TODO: check the url and setting with devops team
mongo_username = os.getenv('MONGO_USERNAME')
mongo_password = os.getenv('MONGO_PASSWORD')
mongo_cluster_url = os.getenv('MONGO_CLUSTER_URL')

mongo_uri = f'mongodb+srv://rapkeb:Aa123456@cluster0.nfbimuj.mongodb.net/'

client = MongoClient(mongo_uri, tls=True, tlsAllowInvalidCertificates=True)
userdb = client['Hackathon']
users_collection = userdb['users']

def add_user(user):
    user_data = {
        "username": user.username,
        "password_hash": user.password_hash,
        "services": user.services
    }
    result = users_collection.insert_one(user_data)
    user.set_id(result.inserted_id)

def find_user_by_email(email):
    return users_collection.find_one({"email": email})

def check_user_password(email, password):
    user = find_user_by_email(email)
    if user and check_password_hash(user['password_hash'], password):
        return True
    return False

def user_from_dict(user_dict):
    user = User(
        username=user_dict['username'],
        email=user_dict['email'],
        password=user_dict['password_hash'],
    )
    user.set_id(user_dict['_id'])
    return user


