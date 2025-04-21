from functools import wraps
from flask import flash, redirect, url_for
from flask_jwt_extended import create_access_token, JWTManager, get_jwt_identity, verify_jwt_in_request
from jwt import ExpiredSignatureError
from App.database import db
from App.models import User

def login(username, password):
  user = User.query.filter_by(username=username).first()
  if user and user.check_password(password):
    return create_access_token(identity=username)
  return None

def signup(username, password):
    if User.query.filter_by(username=username).first():
        raise Exception('Username already exists')
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return new_user

def setup_jwt(app):
    jwt = JWTManager(app)

    @jwt.user_identity_loader
    def user_identity_lookup(identity):
        user = User.query.filter_by(username=identity).one_or_none()
        if user:
           return str(user.id)
        return None

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.get(identity)

    return jwt

def jwt_ignore_expired():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                verify_jwt_in_request()
            except ExpiredSignatureError:
                flash("Token expired, please log in again", "error")
            except Exception:
                return redirect(url_for('auth_views.login_page'))
            return fn(*args, **kwargs)
        return decorator
    return wrapper

# Context processor to make 'is_authenticated' available to all templates
def add_auth_context(app):
  @app.context_processor
  def inject_user():
      try:
          verify_jwt_in_request()
          user_id = get_jwt_identity()
          current_user = User.query.get(user_id)
          is_authenticated = True
      except Exception as e:
          print(e)
          is_authenticated = False
          current_user = None
      return dict(is_authenticated=is_authenticated, current_user=current_user)