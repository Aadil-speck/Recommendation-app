from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt import jwt_required, current_identity
from App.database import db
from sqlalchemy.exc import IntegrityError

from App.controllers import (
    create_user,
    get_all_users,
    get_all_users_json,
    get_user,
    user_signup
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')


# LOGIN - LOGIN ACCOUNT

@user_views.route('/login' , methods=['POST', 'GET'])
def loginAccount():
    data = request.get_json()
    #user_login (data ['email'], data['password'])
    return {"message": "Hello"}


# SIGNUP - CREATE ACCOUNT
@user_views.route('/signup', methods=['POST'])
def createAccount():
    data = request.get_json()
    return {"message": "Hello"}
    return user_signup(data['firstName'], data['lastName'], data['email'], data['password'], data['userType'])



# Routes for testing purposes
# check identity of current user
@user_views.route('/identify', methods=['GET'])
@jwt_required()
def identify_user_action():
    return jsonify({'message': f"id : {current_identity.id}, email: {current_identity.email}, userType: {current_identity.userType}"})

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


# STATIC View all Users
@user_views.route('/static/users', methods=['GET'])
def static_user_page():
  return send_from_directory('static', 'static-user.html')



