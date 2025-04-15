from App.database import db


class RecipeIngredient(db.Model):
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), primary_key=True)
    ingredient_id = db.Column(
        db.Integer, db.ForeignKey("ingredient.id"), primary_key=True
    )
    quantity = db.Column(db.Float, nullable=False) # Quantity of ingredient required for recipe

    def __init__(self, recipe_id, ingredient_id, quantity):
        self.recipe_id = recipe_id
        self.ingredient_id = ingredient_id
        self.quantity = quantity

    def __repr__(self):
        return f"Recipe ID: {self.recipe_id} Ingredient ID: {self.ingredient_id} Quantity: {self.quantity}"
    
    def get_json(self):
        return {
            "recipe_id": self.recipe_id,
            "ingredient_id": self.ingredient_id,
            "quantity": self.quantity
        }