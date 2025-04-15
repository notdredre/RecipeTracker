from App.database import db


class RecipeIngredient(db.Model):
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), primary_key=True)
    ingredient_id = db.Column(
        db.Integer, db.ForeignKey("ingredient.id"), primary_key=True
    )
    quantity = db.Column(db.Float, nullable=False) # Quantity of ingredient required for recipe
