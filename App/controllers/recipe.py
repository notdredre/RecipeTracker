from App.models import Recipe, RecipeIngredient, UserInventory
from App.database import db


def create_recipe(name, description, steps, category, user_id):
    new_recipe = Recipe(name, description, steps, category, user_id)
    db.session.add(new_recipe)
    db.session.commit()
    return new_recipe


def get_recipe(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    return recipe


def get_recipes_by_name(name):
    recipes = Recipe.query.filter_by(name=name).all()
    return recipes

def search_user_recipes(user_id, keywords):
    recipes = []
    for keyword in keywords:
        search_names = Recipe.query.filter(Recipe.name.like(f'%{keyword}%'), Recipe.user_id == user_id).all()
        for recipe in search_names:
            if recipe not in recipes:
                recipes.append(recipe)
        search_desc = Recipe.query.filter(Recipe.description.like(f'%{keyword}%'), Recipe.user_id == user_id).all()
        for recipe in search_desc:
            if recipe not in recipes:
                recipes.append(recipe)
    return recipes

def get_user_recipes(user_id):
    recipes = Recipe.query.filter_by(user_id=user_id).all()
    return recipes


def update_recipe(recipe_id, name, description, steps, ingredients):
    recipe = get_recipe(recipe_id)
    if recipe:
        recipe.name = name
        recipe.description = description
        recipe.steps = steps
        recipe.ingredients = ingredients
        db.session.commit()
        return True
    return False


def delete_recipe(recipe_id):
    recipe = get_recipe(recipe_id)
    if recipe:
        db.session.delete(recipe)
        db.session.commit()
        return True
    return False


def cook_recipe(recipe_id, user_id):
    recipe = get_recipe(recipe_id)
    if recipe:
        recipe_ingredients = RecipeIngredient.query.filter_by(recipe_id=recipe_id).all()
        for recipe_ingredient in recipe_ingredients:
            user_inventory = UserInventory.query.filter_by(
                user_id=user_id, ingredient_id=recipe_ingredient.ingredient_id
            ).first()
            if (
                not user_inventory
                or user_inventory.quantity < recipe_ingredient.quantity
            ):
                return False
            user_inventory.quantity -= recipe_ingredient.quantity
            db.session.add(user_inventory)

        db.session.commit()
        return True
    return False
