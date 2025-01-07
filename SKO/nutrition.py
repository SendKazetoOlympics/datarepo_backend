from flask import Blueprint, request, jsonify, current_app
import psycopg
import psycopg.rows
from database import connect_postgres
from uuid import uuid4

nutrition_service = Blueprint("nutrition", __name__)

@nutrition_service.route("/add_food", methods=["POST"])
def add_food():
    with connect_postgres() as client:
        cursor = client.cursor()
        data = request.form
        same_names = cursor.execute(
            "SELECT * FROM foods WHERE name = %s",
            (data.getlist("name"))
        )
        # if same_names.rowcount > 0:
        #     return jsonify({"message": "Food already exists"})
        # else:
        #     cursor.execute(
        #         "INSERT INTO foods (id, name, calories, protein, fat, carbs) VALUES (gen_random_uuid(), %s, %s, %s, %s, %s)",
        #         (
        #             data.get("name"),
        #             data.get("calories"),
        #             data.get("protein"),
        #             data.get("fat"),
        #             data.get("carbs")
        #         )
        #     )
        return jsonify({"message": "Success"})
        
@nutrition_service.route("/select_food_by_name", methods=["POST"])
def select_food_by_name():
    with connect_postgres() as client:
        cursor = client.cursor()
        data = request.form
        foods = cursor.execute(
            "SELECT * FROM foods WHERE name = %s",
            (data.get("name"))
        )
        return jsonify({"foods": foods.fetchall()})
    
@nutrition_service.route("/add_meal", methods=["POST"])
def add_meal():
    with connect_postgres() as client:
        cursor = client.cursor()
        data = request.form
        cursor.execute(
            "INSERT INTO meals (id, name, date) VALUES (gen_random_uuid(), %s, %s)",
            (
                data.get("name"),
                data.get("date")
            )
        )
        return jsonify({"message": "Success"})