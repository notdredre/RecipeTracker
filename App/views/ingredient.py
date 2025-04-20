from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.controllers.ingredient import (
    get_user_ingredients,
    get_user_ingredient,
    add_user_ingredient,
    update_user_ingredient,
    delete_user_ingredient,
)

ingredient_bp = Blueprint("ingredient", __name__, url_prefix="/ingredients")


@ingredient_bp.route("/", methods=["GET"])
@jwt_required()
def get_ingredients():
    user_id = get_jwt_identity()
    ingredients = get_user_ingredients(user_id)
    return jsonify(
        [
            {"ingredient": ingredient.get_json(), "inventory": inventory.get_json()}
            for ingredient, inventory in ingredients
        ]
    )


@ingredient_bp.route("/", methods=["POST"])
@jwt_required()
def add_ingredient():
    user_id = get_jwt_identity()
    data = request.get_json()
    ingredient_id = data.get("ingredient_id")
    quantity = data.get("quantity")
    if not ingredient_id or not quantity:
        return jsonify({"error": "Ingredient ID and quantity are required"}), 400
    add_user_ingredient(user_id, ingredient_id, quantity)
    return jsonify({"message": "Ingredient added successfully"})


@ingredient_bp.route("/<int:ingredient_id>", methods=["GET"])
@jwt_required()
def get_ingredient(ingredient_id):
    user_id = get_jwt_identity()
    ingredient = get_user_ingredient(user_id, ingredient_id)
    if not ingredient:
        return jsonify({"error": "Ingredient not found"}), 404
    ingredient, inventory = ingredient
    return jsonify(
        {"ingredient": ingredient.get_json(), "inventory": inventory.get_json()}
    )


@ingredient_bp.route("/<int:ingredient_id>", methods=["PUT"])
@jwt_required()
def update_ingredient(ingredient_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    name = data.get("name")
    quantity = data.get("quantity")
    if not quantity:
        return jsonify({"error": "Quantity is required"}), 400
    updated = update_user_ingredient(user_id, ingredient_id, name, quantity)
    if not updated:
        return jsonify({"error": "Ingredient not found"}), 404
    return jsonify({"message": "Ingredient updated successfully"})


@ingredient_bp.route("/<int:ingredient_id>", methods=["DELETE"])
@jwt_required()
def delete_ingredient(ingredient_id):
    user_id = get_jwt_identity()
    deleted = delete_user_ingredient(
        user_id,
        ingredient_id,
    )
    if not deleted:
        return jsonify({"error": "Ingredient not found"}), 404
    return jsonify({"message": "Ingredient deleted successfully"})
