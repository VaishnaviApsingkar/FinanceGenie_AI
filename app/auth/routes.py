from flask import render_template, request, redirect, url_for, flash, jsonify, Blueprint
from flask_login import login_user
from ..models import User
from .. import db
from . import auth_bp
from werkzeug.security import check_password_hash

# auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET'])
def login_page():
    """Render the login page."""
    return render_template('login.html')

@auth_bp.route('/api/login', methods=['POST'])
def api_login():
    try:
        # Parse JSON data from the request
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Check if both username and password are provided
        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400

        # Query the database for the user
        user = User.query.filter_by(username=username).first()

# Validate the user and password
        if not user:
            return jsonify({'error': 'Invalid username or password'}), 401

        
        if user.password != password:
            return jsonify({'error': 'Invalid username or password'}), 401

        login_user(user)
    
        # Ensure transaction table exists
        user.create_transaction_table()

        return jsonify({'message': 'Login successful', 'redirect_url': '/home/dashboard'}), 200

        


    except Exception as e:
        return jsonify({'error': 'An error occurred', 'details': str(e)}), 500
    
