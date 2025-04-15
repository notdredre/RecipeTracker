from App.database import db


class UserInventory(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    ingredient_id = db.Column(
        db.Integer, db.ForeignKey("ingredient.id"), primary_key=True
    )
    quantity = db.Column(
        db.Float, nullable=False
    )  # Quantity of ingredient that user owns. When the user uses a recipe, this should be subtracted from.

    def __init__(self, user_id, ingredient_id, quantity):
        self.user_id = user_id
        self.ingredient_id = ingredient_id
        self.quantity = quantity

    def __repr__(self):
        return f"User ID: {self.user_id} Ingredient ID: {self.ingredient_id} Quantity: {self.quantity}"
    
    def get_json(self):
        return {
            "user_id": self.user_id,
            "ingredient_id": self.ingredient_id,
            "quantity": self.quantity
        }