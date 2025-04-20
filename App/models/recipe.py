from App.database import db


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    steps = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    ingredients = db.relationship("RecipeIngredient", backref="recipe", lazy=True)


    def __init__(self, name, description, steps, category, user_id):
        self.name = name
        self.description = description
        self.steps = steps
        self.category = category
        self.user_id = user_id

    def __repr__(self):
        return f"ID: {self.id} Name: {self.name} Description: {self.description} Steps: {self.steps} Category: {self.category} User ID: {self.user_id} Ingredients: {self.ingredients}"
    
    def get_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "steps": self.steps,
            "category": self.category,
            "user_id": self.user_id,
            "ingredients": [ingredient.get_json() for ingredient in self.ingredients]
        }