from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from App.controllers.recipe import *
from App.controllers.ingredient import get_missing_ingredients

recipe_views = Blueprint('recipe_views', __name__, template_folder='../templates')

@recipe_views.route('/recipes', methods=['GET'])
@jwt_required
def get_recipes_page():
    recipes = get_user_recipes(jwt_current_user.id)
    return jsonify(recipes=recipes)

@recipe_views.route('/recipes', methods=['POST'])
@jwt_required
def add_recipe_action():
    data = request.form
    create_recipe(data['name'], data['description'], data['steps'], jwt_current_user.id)
    flash("Recipe created successfully!")
    return jsonify(data=data)

@recipe_views.route('/recipes/<int:recipe_id>', methods=['GET'])
@jwt_required
def get_recipe_detail_page(recipe_id):
    recipe = get_recipe(recipe_id)
    missing_ingredients = get_missing_ingredients(jwt_current_user.id, recipe_id)
    return jsonify(recipe=recipe, missing_ingredients=missing_ingredients)

@recipe_views.route('/recipes/<int:recipe_id>', methods=['PUT'])
@jwt_required
def update_recipe_action(recipe_id):
    data = request.form
    recipe = get_recipe(recipe_id)
    if recipe:
        # update recipe controller
        flash("Updated recipe successfully!")
    else:
        flash("Could not update recipe!", "error")
    return redirect(request.referrer)

@recipe_views.route('/recipes/<int:recipe_id>', methods=['DELETE'])
@jwt_required
def delete_recipe_action(recipe_id):
    recipe = get_recipe(recipe_id)
    if recipe:
        # delete recipe controller
        flash("Deleted recipe successfully")
    else:
        flash("Could not delete recipe!", "error")
    return redirect(request.referrer)