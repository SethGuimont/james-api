import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from json2html import *
from constants import *
load_dotenv()

app = Flask(__name__)
CORS(app)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

'''Begin routes for HTML templates'''


@app.route("/")
def home():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_POSTS)
            menu_items = cursor.fetchall()
            cursor.close()
    return render_template("index.html", menu_items=menu_items)


'''Begin API Functionality'''


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


@app.route("/api/menuitems/<int:id>", methods=["DELETE"])
def delete_menuitem(id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(DELETE_MENUITEM_BY_ID, (id,))
            if cursor.rowcount == 0:
                return jsonify({"error": f"menu item with ID {id} not found."}), 404
        return jsonify({"message": f"menu item with ID {id} deleted."})


if __name__ == "__main__":
    app.run()
