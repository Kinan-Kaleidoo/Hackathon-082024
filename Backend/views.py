import os
from flask import render_template, request, redirect, session, url_for, jsonify
import requests
from db import  find_user_by_email, users_collection
# import pandas as pd
# import yfinance as yf
# import datetime as dt
# import numpy as np
# import pandas as pd
# from matplotlib import style
# from statsmodels.tsa.seasonal import STL
# from sklearn.metrics import mean_squared_error, accuracy_score
# from iexfinance.stocks import Stock
from flask_login import login_required
from db import find_user_by_email


from flask_login import login_required
from bson.objectid import ObjectId


# _df = pd.read_csv('companylist.csv')
# df = _df.copy()

def login():
    return render_template('login.html')


@login_required
def index():

    return render_template('index.html')

@login_required
def media():
    return render_template('index.html')

@login_required
def search():
    return render_template('index.html')

@login_required
def doc():
    return render_template('index.html')

@login_required
def audio():
    return render_template('index.html')

@login_required
def video():
    return render_template('index.html')