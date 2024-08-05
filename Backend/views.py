import os
from flask import render_template, request, redirect, session, url_for, jsonify
import requests
from db import  find_user_by_username, users_collection
import pandas as pd
import yfinance as yf
import datetime as dt
import numpy as np
import pandas as pd
from matplotlib import style
from statsmodels.tsa.seasonal import STL
from sklearn.metrics import mean_squared_error, accuracy_score
from iexfinance.stocks import Stock
from flask_login import login_required
from db import find_user_by_username, update_prefernces, buy_share1, get_user_purchases


from flask_login import login_required
from bson.objectid import ObjectId


_df = pd.read_csv('companylist.csv')
df = _df.copy()

def login():
    return render_template('login.html')


@login_required
def company_chart():
    company_name = request.args.get('company')
    share = request.args.get('share')  
    actual_date = dt.date.today()
    past_date = actual_date - dt.timedelta(days=365 * 5)
    actual_date = actual_date.strftime("%Y-%m-%d")
    past_date = past_date.strftime("%Y-%m-%d")
    data = yf.download(share, start=past_date, end=actual_date)
    df = pd.DataFrame(data).reset_index()
    # company_data = df[df['Company'] == company_name]
    def format_data(company_data):
        return {
            'dates': company_data['Date'].tolist(),
            'closes': company_data['Close'].tolist(),
            'opens': company_data['Open'].tolist(),
            'highs': company_data['High'].tolist(),
            'lows': company_data['Low'].tolist()
        }
    data = format_data(df)
    return render_template('chart.html', company=company_name, share=share,  data1=data)

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