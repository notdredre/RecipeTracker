from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from App.controllers.recipe import *
from App.controllers.ingredient import (
    get_missing_ingredients,
    add_recipe_ingredient,
    delete_recipe_ingredient,
    create_ingredient,
)

recipe_views = Blueprint('recipe_views', __name__, template_folder='../templates')

@recipe_views.route('/recipes', methods=['POST'])
@jwt_required()
def add_recipe_action():
    data = request.form
    ingredients = []
    for field in data:
        if "ingredient_names" in field:
            num = field[len("ingredient_names"):]
            ingredients.append((data[f"ingredient_names{num}"], data[f"ingredient_quantities{num}"]))
    new_recipe = create_recipe(data['name'], data['description'], data['steps'], data['category'], jwt_current_user.id)
    for name, quantity in ingredients:
        new_ingredient = create_ingredient(name)
        add_recipe_ingredient(new_recipe.id, new_ingredient.id, quantity)
    flash("Recipe created successfully!")
    return jsonify(data=data)

@recipe_views.route('/recipes/<int:recipe_id>', methods=['GET'])
@jwt_required()
def get_recipe_detail_page(recipe_id):
    recipe = get_recipe(recipe_id)
    missing_ingredients = get_missing_ingredients(jwt_current_user.id, recipe_id)
    return jsonify(recipe=recipe.get_json(), missing_ingredients=[(ingredient.get_json(), quantity) for ingredient, quantity in missing_ingredients])

@recipe_views.route('/recipes/<int:recipe_id>', methods=['POST']) #Change this
@jwt_required()
def update_recipe_action(recipe_id):
    data = request.form
    recipe = get_recipe(recipe_id)
    if recipe:
        for recipe_ingredient in recipe.ingredients:
            delete_recipe_ingredient(recipe.id, recipe_ingredient.ingredient_id)
        form_ingredients = []
        for field in data:
            if "ingredient_names" in field:
                num = field[len("ingredient_names"):]
                form_ingredients.append((data[f"ingredient_names{num}"], data[f"ingredient_quantities{num}"]))
        for name, quantity in form_ingredients:
            ingredient = create_ingredient(name)
            add_recipe_ingredient(recipe_id, ingredient.id, quantity)
        if update_recipe(recipe_id, data['name'], recipe.description, recipe.steps):
            flash("Updated recipe successfully!")
        else:
            flash("Could not update recipe!", "error")
    else:
        flash("Recipe does not exist!", "error")
    return redirect(request.referrer)

@recipe_views.route('/recipes/<int:recipe_id>/delete', methods=['POST'])
@jwt_required()
def delete_recipe_action(recipe_id):
    recipe = get_recipe(recipe_id)
    if recipe:
        if delete_recipe(recipe_id):
            flash("Deleted recipe successfully")
        else:
            flash("Could not delete recipe!", "error")
    else:
        flash("Recipe does not exist!", "error")
    return redirect(url_for('index_views.home_page'))


@recipe_views.route('/recipes/<int:recipe_id>/cook', methods=['POST'])
@jwt_required()
def cook_recipe_action(recipe_id):
    recipe = get_recipe(recipe_id)
    if recipe:
        if cook_recipe(recipe_id, jwt_current_user.id):
            flash('Recipe cooked successfully! Ingredients have been deducted from your inventory.')
        else:
            flash('Cannot cook recipe - insufficient ingredients!', 'error')
    else:
        flash('Recipe not found!', 'error')
    return redirect(url_for('index_views.home_page'))
