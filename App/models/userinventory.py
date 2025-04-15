from App.database import db


class UserInventory(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    ingredient_id = db.Column(
        db.Integer, db.ForeignKey("ingredient.id"), primary_key=True
    )
    quantity = db.Column(
        db.Float, nullable=False
    )  # Quantity of ingredient that user owns. When the user uses a recipe, this should be subtracted from.
