from flask import Blueprint, request, jsonify, current_app
import psycopg
import psycopg.rows

database_service = Blueprint("database", __name__)

def connect_postgres() -> psycopg.Connection[psycopg.rows.TupleRow]:
    database_client = psycopg.connect(
        host=current_app.config["POSTGRES_HOST"],
        port=current_app.config["POSTGRES_PORT"],
        user=current_app.config["POSTGRES_USER"],
        password=current_app.config["POSTGRES_PASSWORD"],
        dbname=current_app.config["POSTGRES_DB"],
        row_factory=psycopg.rows.dict_row
    )
    return database_client

@database_service.route("/upload_video", methods=["POST"])
def upload_video():
    with connect_postgres() as client:
        cursor = client.cursor()
        data = request.form
        same_names = cursor.execute(
            "SELECT * FROM videos WHERE name = %s",
            (data.getlist("name"))
        )
        if same_names.rowcount > 0:
            return jsonify({"message": "Video already exists"})
        else:
            cursor.execute(
                "INSERT INTO videos (id, name, start_time, camera) VALUES (gen_random_uuid(), %s, %s, %s)",
                (
                    data.get("name"),
                    data.get("start_time"),
                    data.get("camera")
                )
            )
            return jsonify({"message": "Success"})

@database_service.route("/select_video_by_date", methods=["POST"])
def select_video_by_date():
    with connect_postgres() as client:
        cursor = client.cursor()
        data = request.form
        videos = cursor.execute(
            "SELECT * FROM videos WHERE cast(to_timestamp(start_time/1000) as date) BETWEEN %s AND %s ORDER BY start_time DESC",
            (
                data.get("start_date"),
                data.get("end_date")
            )
        )
        return jsonify({"videos": videos.fetchall()})

@database_service.route("/select_video_by_type", methods=["GET"])
def select_video_by_type():
    pass

@database_service.route("/select_video_by_name", methods=["GET"])
def select_video_by_name():
    pass
