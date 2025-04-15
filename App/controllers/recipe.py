from App.models import Recipe, RecipeIngredient, Ingredient
from App.database import db

def create_recipe(name, description, steps, user_id):
    new_recipe = Recipe(name, description, steps, user_id)
    db.session.add(new_recipe)
    db.session.commit()

def get_recipe(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    return recipe

def get_recipes_by_name(name):
    recipes = Recipe.query.filter_by(name=name).all()
    return recipes

def get_user_recipes(user_id):
    recipes = Recipe.query.filter_by(user_id=user_id).all()
    return recipes