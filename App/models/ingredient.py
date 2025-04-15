from App.database import db


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"ID: {self.id} Name: {self.name}"
    
    def get_json(self):
        return {
            "id": self.id,
            "name": self.name
        }