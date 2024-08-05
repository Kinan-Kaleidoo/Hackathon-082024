import os
from flask import render_template, request, redirect, session, url_for, jsonify
import requests
from db import  find_user_by_username, users_collection

from flask_login import login_required
from db import find_user_by_username, update_prefernces, buy_share1, get_user_purchases
import magic



from flask_login import login_required
from bson.objectid import ObjectId


_df = pd.read_csv('companylist.csv')
df = _df.copy()

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
    if request.method == "POST":
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        if file:
            file_content = file.read()
            mime = magic.Magic(mime=True)
            file_type = mime.from_buffer(file_content)
            if file_type in ["application/pdf", "text/plain", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
                return jsonify({"filename": file.filename, "format": file_type}), 200
            else:
                return jsonify({"error": "File is not a PDF, TXT, or WORD document", "file_type": file_type}), 400
        return jsonify({"error": "No file provided"}), 400
    else:
        return jsonify("good"), 200


@login_required
def audio():
    return render_template('index.html')

@login_required
def video():
    return render_template('index.html')