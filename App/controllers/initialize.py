from .user import create_user
from .recipe import *
from .ingredient import *

from App.database import db


def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    create_recipe("Pasta", "Pasta dish", "1. Kraft Mac n Cheese", "salty", 1)
    create_ingredient("Kraft Mac n Cheese")
    create_ingredient("bob's sauce")
    add_recipe_ingredient(1, 1, 100)
    add_user_ingredient(1, 2, 2000)
    print(get_missing_ingredients(1, 1))