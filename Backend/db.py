from datetime import datetime
from flask import jsonify, request, session
from models import check_password_hash
from models import User
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import pandas as pd
from flask_login import current_user

load_dotenv()

mongo_username = os.getenv('MONGO_USERNAME')
mongo_password = os.getenv('MONGO_PASSWORD')
mongo_cluster_url = os.getenv('MONGO_CLUSTER_URL')

mongo_uri = f'mongodb+srv://rapkeb:Aa123456@cluster0.nfbimuj.mongodb.net/'

client = MongoClient(mongo_uri, tls=True, tlsAllowInvalidCertificates=True)
userdb = client['StockDB']
users_collection = userdb['users']
purchases_collection = userdb['purchases']

def add_user(user):
    user_data = {
        "username": user.username,
        "password_hash": user.password_hash,
        "services": user.services
    }
    result = users_collection.insert_one(user_data)
    user.set_id(result.inserted_id)

def find_user_by_username(username):
    return users_collection.find_one({"username": username})

def check_user_password(username, password):
    user = find_user_by_username(username)
    if user and check_password_hash(user['password_hash'], password):
        return True
    return False

def user_from_dict(user_dict):
    user = User(
        username=user_dict['username'],
        password=user_dict['password_hash'],
    )
    user.set_id(user_dict['_id'])
    user.services = user_dict['services']
    return user

def update_prefernces(username, selected_sectors, risk_tolerance, investment_horizon):
    # Update user preferences in MongoDB
    users_collection.update_one(
        {'username': username},
        {'$set': {
            'preferences.sectors': selected_sectors,
            'preferences.risk_tolerance': risk_tolerance,
            'preferences.investment_horizon': investment_horizon
        }}
    )

def buy_share1(company, share, quantity, price):
    # Create a purchase document
    quantity = int(quantity)  # Convert quantity to an integer
    price = float(price)  # Convert price to a float
    purchase = {
        'username': session['username'],
        'company': company,
        'share': share,
        'quantity': quantity,
        'price': price,
        'total_cost': quantity * price,
        'timestamp': datetime.now()
    }
    # Insert the purchase document into the purchases collection
    purchases_collection.insert_one(purchase)
    return jsonify({'status': 'success', 'message': 'Purchase saved successfully'}), 200

def get_user_purchases():
    lst = purchases_collection.find({'username': session['username']})
    return lst


