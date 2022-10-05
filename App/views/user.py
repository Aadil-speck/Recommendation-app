from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt import jwt_required
from App.database import db
from sqlalchemy.exc import IntegrityError

from App.controllers import (
    user_signup,
    get_all_users,
    get_all_users_json,
    get_user,
    create_user,
    login_user
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')

# View all Users
@user_views.route('/view/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

# JSON View all Users
@user_views.route('/users')
def client_app():
    users = get_all_users_json()
    return jsonify(users)

@user_views.route('/static/users')
def static_user_page():
  return send_from_directory('static', 'static-user.html')

# SIGNUP
@user_views.route('/signup', methods=['POST'])
def signup():
    userdata = request.get_json()
    return user_signup(userdata)
