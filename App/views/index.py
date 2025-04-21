from flask import Blueprint, redirect, render_template, jsonify, url_for, request
from App.controllers import initialize
from App.controllers.recipe import get_user_recipes, search_user_recipes
from App.controllers.ingredient import get_recipe_ingredients
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
@jwt_required(optional=True)
def index_page():
    if jwt_current_user:
        return redirect(url_for('index_views.home_page'))
    return render_template('login.html')

@index_views.route('/init', methods=['GET'])
def init():
    initialize()
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})

@index_views.route('/home', methods=['GET'])
@jwt_required()
def home_page():
    query = request.args.get('search')
    if query:
        query = query.split(' ')
        all_recipes = search_user_recipes(jwt_current_user.id, query)
    else:
        all_recipes = get_user_recipes(jwt_current_user.id)
    recipes = []
    for recipe in all_recipes:
        recipe_ingredients = get_recipe_ingredients(recipe.id)
        recipes.append((recipe, recipe_ingredients))
    return render_template("recipes.html", recipes=recipes)