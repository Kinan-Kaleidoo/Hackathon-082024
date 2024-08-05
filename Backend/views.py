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
    unique_companies = df[['Company', 'Sector', 'Share', 'Industry']].drop_duplicates().sort_values(by='Company')
    unique_companies_list = unique_companies.to_dict(orient='records')
    return render_template('index.html', companies=unique_companies_list)

@login_required
def compare_shares():
    company1_name = request.args.get('company1')
    company2_name = request.args.get('company2')

    actual_date = dt.date.today()
    past_date = actual_date - dt.timedelta(days=365 * 5)
    actual_date = actual_date.strftime("%Y-%m-%d")
    past_date = past_date.strftime("%Y-%m-%d")
    share1 = df.loc[df['Company'] == company1_name, 'Share'].values[0]
    share2 = df.loc[df['Company'] == company2_name, 'Share'].values[0]
    data1 = yf.download(share1, start=past_date, end=actual_date)
    data2 = yf.download(share2, start=past_date, end=actual_date)

    company1_data = pd.DataFrame(data1).reset_index()
    company2_data = pd.DataFrame(data2).reset_index()

    def format_data(company_data):
        return {
            'dates': company_data['Date'].tolist(),
            'closes': company_data['Close'].tolist(),
            'opens': company_data['Open'].tolist(),
            'highs': company_data['High'].tolist(),
            'lows': company_data['Low'].tolist()
        }

    data1 = format_data(company1_data)
    data2 = format_data(company2_data)

    return render_template('compare_shares.html', company1=company1_name, data1=data1, company2=company2_name, data2=data2)

@login_required
def buy_share():
    data = request.json
    company = data.get('company')
    share = data.get('share')
    quantity = data.get('quantity')
    price = data.get('price')

    if not all([company, share, quantity, price]):
        return jsonify({'status': 'error', 'message': 'Missing data fields'}), 400
    buy_share1(company, share, quantity, price)
    return jsonify({'status': 'success', 'message': 'Purchase saved successfully'}), 200

@login_required
def get_current_price(symbol):
    try:
        stock = yf.Ticker(symbol)
        history = stock.history(period="1d")
        
        # Check if history DataFrame is empty
        if history.empty:
            raise ValueError(f"No data available for symbol: {symbol}")
        
        return history['Close'].iloc[-1]
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None
    
@login_required
def recommendation():
    # Retrieve company parameter from request
    company = request.args.get('company')
    # Retrieve Finnhub API key from environment variables
    api_key = os.getenv('FINNHUB_API_KEY')
    # Construct the URL with the company symbol and API key
    url = f'https://finnhub.io/api/v1/stock/recommendation?symbol={company}&token={api_key}'
    # Make the request to the Finnhub API
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        # Return the JSON response
        return jsonify(response.json())
    else:
        # Return an error message if the request failed
        return jsonify({'error': 'Failed to fetch recommendations'}), response.status_code
    

@login_required
def current_price():
    company = request.args.get('company')
    price = get_current_price(company)
    if price is not None:
        return jsonify({'price': price})
    else:
        return jsonify({'error': 'Unable to fetch price'}), 500
    
@login_required
def preferences():
    if request.method == 'POST':
        # Update user preferences
        selected_sectors = request.form.getlist('sectors')
        risk_tolerance = request.form.get('risk_tolerance')
        investment_horizon = request.form.get('investment_horizon')

        # Assuming 'username' is stored in the session or provided in some other way
        username = session['username']

        # Update user preferences in MongoDB
        update_prefernces(username, selected_sectors, risk_tolerance, investment_horizon)
        return redirect(url_for('preferences'))

    # Fetch current preferences
    sectors = df['Sector'].unique().tolist()
    username = session['username']
    user = find_user_by_username(username)
    preferences = user.get('preferences', {})
    return render_template('preferences.html', preferences=preferences, sectors=sectors)

@login_required
def predict():
    date = request.args.get('date')
    share = request.args.get('share')

    if not date or not share:
        return jsonify({"error": "Missing date or share parameter"}), 400

    # Add your logic to predict based on date and share
    # Example: prediction = your_prediction_function(date, share)
    actual_date = dt.date.today()
    past_date = actual_date - dt.timedelta(days=365 * 3)

    actual_date = actual_date.strftime("%Y-%m-%d")
    past_date = past_date.strftime("%Y-%m-%d")

    print("Retrieving Stock Data from introduced symbol...")
    stock_dataframe = get_stock_data(share, past_date, actual_date)

    print("Retrieving Gold Data...")
    gold_dataframe = get_gold_data(past_date, actual_date)

    print("Retrieving Forex Data (EUR/USD)...")
    forex_dataframe = get_forex_data(past_date, actual_date)

    print("Merging Stock, Gold, and Forex Data...")
    merged_dataframe = pd.merge(stock_dataframe, gold_dataframe, left_index=True, right_index=True)
    merged_dataframe = pd.merge(merged_dataframe, forex_dataframe, left_index=True, right_index=True)

    print("Forecasting with merged DataFrame using STL...")
    forecast, trend, seasonal, resid = stl_forecast(merged_dataframe)
    print("Calculating trend-based accuracy...")
    trend_accuracy = calculate_trend_accuracy(merged_dataframe, forecast)
    print(f"Trend-based accuracy: {trend_accuracy}")

    # Today's forecasted close price
    todays_forecast = forecast[-1]
    print(f"Forecasted close price for today: {todays_forecast}")

    # Here, replace with your actual prediction logic
    prediction = f"Predicted value for {share} on {date} is {todays_forecast}"

    return jsonify({"prediction": prediction})


def get_stock_data(symbol, from_date, to_date):
    data = yf.download(symbol, start=from_date, end=to_date)
    df = pd.DataFrame(data)
    print(df.head())
    df['HighLoad'] = (df['High'] - df['Close']) / df['Close'] * 100.0
    df['Change'] = (df['Close'] - df['Open']) / df['Open'] * 100.0

    df['Price_Up'] = df['Close'].diff().fillna(0) > 0  # True if price went up, else False

    df['MA_5'] = df['Close'].rolling(window=5).mean()  # 5-day Moving Average
    df['MA_20'] = df['Close'].rolling(window=20).mean()  # 20-day Moving Average
    df['RSI'] = calculate_rsi(df['Close'])  # Relative Strength Index
    df['MACD'] = calculate_macd(df['Close'])  # MACD
    df['Bollinger_Upper'], df['Bollinger_Lower'] = calculate_bollinger_bands(df['Close'])  # Bollinger Bands

    df = df[['Close', 'HighLoad', 'Change', 'Volume', 'MA_5', 'MA_20', 'RSI', 'MACD', 'Bollinger_Upper', 'Bollinger_Lower', 'Price_Up']]
    df = df.dropna()  # Drop rows with NaN values due to moving averages
    return df

def get_gold_data(from_date, to_date):
    gold_data = yf.download('GC=F', start=from_date, end=to_date)
    gold_df = pd.DataFrame(gold_data)
    gold_df['Gold_HighLoad'] = (gold_df['High'] - gold_df['Close']) / gold_df['Close'] * 100.0
    gold_df['Gold_Change'] = (gold_df['Close'] - gold_df['Open']) / gold_df['Open'] * 100.0

    gold_df['Gold_Price_Up'] = gold_df['Close'].diff().fillna(0) > 0  # True if gold price went up, else False

    gold_df = gold_df[['Close', 'Gold_HighLoad', 'Gold_Change', 'Volume', 'Gold_Price_Up']]
    gold_df = gold_df.dropna()
    gold_df = gold_df.rename(columns={'Close': 'Gold_Close', 'Volume': 'Gold_Volume'})
    return gold_df

def get_forex_data(from_date, to_date):
    forex_data = yf.download('EURUSD=X', start=from_date, end=to_date)
    forex_df = pd.DataFrame(forex_data)
    forex_df['EURUSD_HighLoad'] = (forex_df['High'] - forex_df['Close']) / forex_df['Close'] * 100.0
    forex_df['EURUSD_Change'] = (forex_df['Close'] - forex_df['Open']) / forex_df['Open'] * 100.0

    forex_df['EURUSD_Price_Up'] = forex_df['Close'].diff().fillna(0) > 0  # True if EUR/USD rate went up, else False

    forex_df = forex_df[['Close', 'EURUSD_HighLoad', 'EURUSD_Change', 'Volume', 'EURUSD_Price_Up']]
    forex_df = forex_df.dropna()
    forex_df = forex_df.rename(columns={'Close': 'EURUSD_Close', 'Volume': 'EURUSD_Volume'})
    return forex_df

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(series, short_window=12, long_window=26, signal_window=9):
    short_ema = series.ewm(span=short_window, adjust=False).mean()
    long_ema = series.ewm(span=long_window, adjust=False).mean()
    macd = short_ema - long_ema
    signal = macd.ewm(span=signal_window, adjust=False).mean()
    return macd - signal

def calculate_bollinger_bands(series, window=20, num_std_dev=2):
    rolling_mean = series.rolling(window).mean()
    rolling_std = series.rolling(window).std()
    upper_band = rolling_mean + (rolling_std * num_std_dev)
    lower_band = rolling_mean - (rolling_std * num_std_dev)
    return upper_band, lower_band

def stl_forecast(df, steps=30, period=30):
    stl = STL(df['Close'], period=period, seasonal=13)
    result = stl.fit()

    trend = result.trend
    seasonal = result.seasonal
    resid = result.resid

    trend_forecast = [trend[-1]] * steps
    seasonal_forecast = list(seasonal[-period:]) * (steps // period + 1)
    seasonal_forecast = seasonal_forecast[:steps]
    forecast = np.array(trend_forecast) + np.array(seasonal_forecast)

    # plt.figure(figsize=(12, 8))
    # plt.subplot(411)
    # plt.plot(df.index, df['Close'], label='Original')
    # plt.legend(loc='best')
    # plt.subplot(412)
    # plt.plot(df.index, trend, label='Trend')
    # plt.legend(loc='best')
    # plt.subplot(413)
    # plt.plot(df.index, seasonal, label='Seasonality')
    # plt.legend(loc='best')
    # plt.subplot(414)
    # plt.plot(df.index, resid, label='Residuals')
    # plt.legend(loc='best')
    # plt.tight_layout()
    # plt.show()

    actual = df['Close'][-steps:].values
    mse = mean_squared_error(actual, forecast[-steps:])
    print(f'STL Forecast MSE: {mse}')

    return forecast, trend, seasonal, resid


def calculate_trend_accuracy(df, forecast):
    forecast_trend = np.sign(np.diff(forecast))
    actual_trend = np.sign(np.diff(df['Close'].values[-len(forecast):]))
    accuracy = accuracy_score(actual_trend > 0, forecast_trend > 0)
    return accuracy

@login_required
def purchases():
    # Retrieve all purchases for the current user from the database
    purchases = get_user_purchases()
    # Convert MongoDB cursor to list
    purchase_list = list(purchases)
    return render_template('purchases.html', purchases=purchase_list)
