from flask import Flask
from urls import configure_routes
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_fallback_secret_key')

configure_routes(app)

if __name__ == "__main__":
    app.run('0.0.0.0', port=5005)