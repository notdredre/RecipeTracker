from App.models import RecipeIngredient, UserInventory, Ingredient
from App.database import db

def create_ingredient(name):
    exists = get_ingredient_by_name(name)
    if not exists:
        new_ingredient = Ingredient(name)
        db.session.add(new_ingredient)
        db.session.commit()

def get_ingredient(ingredient_id):
    ingredient = Ingredient.query.filter_by(ingredient_id=ingredient_id).first()
    return ingredient

def get_ingredient_by_name(name):
    ingredient = Ingredient.query.filter_by(name=name).first()
    return ingredient

def update_ingredient(ingredient_id, name):
    ingredient = get_ingredient(ingredient_id)
    if ingredient:
        ingredient.name = name
        db.session.commit()
        return True
    return False

def add_recipe_ingredient(recipe_id, ingredient_id, quantity):
    new_recipe_ingredient = RecipeIngredient(recipe_id, ingredient_id, quantity)
    db.session.add(new_recipe_ingredient)
    db.session.commit()

def get_recipe_ingredients(recipe_id):
    ingredients = db.session.query(Ingredient, RecipeIngredient).filter(RecipeIngredient.recipe_id == recipe_id).join(Ingredient, RecipeIngredient.ingredient_id == Ingredient.id).all()
    return ingredients

def get_recipe_ingredient(recipe_id, ingredient_id):
    ingredient = db.session.query(Ingredient, RecipeIngredient).filter(RecipeIngredient.recipe_id == recipe_id, RecipeIngredient.ingredient_id == ingredient_id).join(Ingredient, RecipeIngredient.ingredient_id == Ingredient.id).first()
    return ingredient

def delete_recipe_ingredient(recipe_id, ingredient_id):
    if get_recipe_ingredient(recipe_id, ingredient_id):
        _, recipe_ingredient = get_recipe_ingredient(recipe_id, ingredient_id)
        db.session.delete(recipe_ingredient)
        db.session.commit()
        return True
    return False

def update_recipe_ingredient(recipe_id, ingredient_id, name, quantity):
    if get_recipe_ingredient(recipe_id, ingredient_id):
        ingredient, recipe_ingredient = get_recipe_ingredient(recipe_id, ingredient_id)
        ingredient.name = name
        recipe_ingredient.quantity = quantity
        db.session.commit()
        return True
    return False

def add_user_ingredient(user_id, ingredient_id, quantity):
    new_user_ingredient = UserInventory(user_id, ingredient_id, quantity)
    db.session.add(new_user_ingredient)
    db.session.commit()

def get_user_ingredients(user_id):
    ingredients = db.session.query(Ingredient, UserInventory).filter(UserInventory.user_id == user_id).join(Ingredient, UserInventory.ingredient_id == Ingredient.id).all()
    return ingredients

def get_user_ingredient(user_id, ingredient_id):
    ingredient = db.session.query(Ingredient, UserInventory).filter(UserInventory.user_id == user_id, UserInventory.ingredient_id == ingredient_id).join(Ingredient, UserInventory.ingredient_id == Ingredient.id).first()
    return ingredient

def delete_user_ingredient(user_id, ingredient_id):
    if get_user_ingredient(user_id, ingredient_id):
        _, inventory = get_user_ingredient(user_id, ingredient_id)
        db.session.delete(inventory)
        db.session.commit()
        return True
    return False

def update_user_ingredient(user_id, ingredient_id, name, quantity):
    if get_user_ingredient(user_id, ingredient_id):
        ingredient, inventory = get_user_ingredient(user_id, ingredient_id)
        ingredient.name = name
        inventory.quantity = quantity
        db.session.commit()
        return True
    return False

def get_missing_ingredients(user_id, recipe_id):
    recipe_ingredients = get_recipe_ingredients(recipe_id)
    missing_ingredients = []
    for ingredient, recipe_ingredient in recipe_ingredients:
        if get_user_ingredient(user_id, ingredient.id):
            _, user_inventory = get_user_ingredient(user_id, ingredient.id)
            diff = recipe_ingredient.quantity - user_inventory.quantity
            if diff > 0:
                missing_ingredients.append((ingredient, diff))
        else:
            missing_ingredients.append((ingredient, recipe_ingredient.quantity))
    return missing_ingredients