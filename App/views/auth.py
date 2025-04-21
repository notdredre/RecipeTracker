from flask import Blueprint, render_template, jsonify, request, flash, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies

from App.controllers.auth import signup


from.index import index_views

from App.controllers import (
    login
)

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')




'''
Page/Action Routes
'''    
@auth_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@auth_views.route('/identify', methods=['GET'])
@jwt_required()
def identify_page():
    return render_template('message.html', title="Identify", message=f"You are logged in as {current_user.id} - {current_user.username}")
    

@auth_views.route('/login', methods=['POST'])
def login_action():
    data = request.form
    token = login(data['username'], data['password'])
    if not token:
        flash('Bad username or password given'), 401
        response = redirect(url_for('auth_views.login_page'))
    else:
        flash('Login Successful')
        response = redirect(url_for('index_views.home_page'))
        set_access_cookies(response, token) 
    return response


@auth_views.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')


@auth_views.route('/logout', methods=['GET'])
def logout_action():
    response = redirect(url_for('index_views.index_page'))
    flash("Logged Out!")
    unset_jwt_cookies(response)
    return response

@auth_views.route('/signup', methods=['GET'])
def signup_page():
    return render_template('signup.html')

@auth_views.route('/signup', methods=['POST'])
def signup_action():
    data = request.form
    try:
        signup(data['username'], data['password'])
        flash('Account created successfully!')
        return login_action()
    except Exception as e:
        flash('Error creating account. Username may be taken.')
        return redirect(url_for('auth_views.signup_page'))
    

'''
API Routes
'''

@auth_views.route('/api/login', methods=['POST'])
def user_login_api():
  data = request.json
  token = login(data['username'], data['password'])
  if not token:
    return jsonify(message='bad username or password given'), 401
  response = jsonify(access_token=token) 
  set_access_cookies(response, token)
  return response

@auth_views.route('/api/identify', methods=['GET'])
@jwt_required()
def identify_user():
    return jsonify({'message': f"username: {current_user.username}, id : {current_user.id}"})

@auth_views.route('/api/logout', methods=['GET'])
def logout_api():
    response = jsonify(message="Logged Out!")
    unset_jwt_cookies(response)
    return response