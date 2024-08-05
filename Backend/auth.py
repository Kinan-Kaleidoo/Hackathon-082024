from db import add_user, find_user_by_email, check_user_password, users_collection, user_from_dict
from flask_login import login_user, logout_user, login_required
from flask import jsonify, request, session
from models import User


@login_required
def logout():
    session.clear()
    logout_user()
    return jsonify({"success": True, "message": "Logout successful"}), 200


def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        user_dict = find_user_by_email(email)
        if user_dict and check_user_password(email, password):
            user = user_from_dict(user_dict)
            session['email'] = user.email
            session['user_id'] = str(user._id)
            session['is_logged_in'] = True
            login_user(user)
            return jsonify({"success": True, "message": "Login successful", "username": str(user.username), "user_id": str(user._id)}), 200
        else:
            return jsonify({"success": False, "message": "Invalid email or password"}), 401


def is_password_legal(password):
    if len(password) < 8:
        return False
    special_characters = "!@#&%()"
    if not any(char in special_characters for char in password):
        return False
    return True


def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if not all([username, email, password, confirm_password]):  # Check if any field is missing
            return jsonify({"success": False, "message": "All fields are required"}), 400
        if not is_password_legal(password):
            return jsonify({"success": False, "message": "Password must be longer then 8 chars and include special character"}), 400
        if password != confirm_password:
            return jsonify({"success": False, "message": "Passwords do not match"}), 400

        existing_user = users_collection.find_one({"$or": [{"email": email}]})
        if existing_user:
            return jsonify({"success": False, "message": "User already exists"}), 400

        new_user = User(username=username, email=email, password=password)
        add_user(new_user)
        return jsonify({"success": True, "message": "User registered successfully"}), 201
