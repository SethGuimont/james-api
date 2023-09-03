import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from json2html import *

load_dotenv()

SELECT_ALL_POSTS = "SELECT * FROM menu_item;"
INSERT_MENUITEM_RETURN_ID = "INSERT INTO menu_item (name, description) VALUES (%s, %s) RETURNING id;"

app = Flask(__name__)
CORS(app)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)


@app.route("/")
def home():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_POSTS)
            menu_items = cursor.fetchall()
            cursor.close()
    return render_template("index.html", menu_items=menu_items)


@app.route("/api/menuitems", methods=["POST"])
def create_menuitem():
    data = request.get_json()
    name = data["name"]
    description = data["description"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_MENUITEM_RETURN_ID, (name, description,))
            id = cursor.fetchone()[0]
    return {"id": id, "name": name, "message": f"menu item {name} created."}, 201


@app.route("/api/menuitems", methods=["GET"])
def get_all_users():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_POSTS)
            menu_items = cursor.fetchall()
            if menu_items:
                result = []
                for item in menu_items:
                    result.append({"name": item[1], "description": item[2]})
                return jsonify(result)
            else:
                return jsonify({"error": f"Users not found."}), 404



if __name__ == "__main__":
    app.run()
