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


# informational static pages
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/location")
def location():
    return render_template("location.html")


@app.route("/partners")
def partners():
    return render_template("partners.html")


# Pages with dynamic data
@app.route("/bakery")
def bakery():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_BAKERY)
            bakery = cursor.fetchall()
            cursor.close()
    return render_template("bakery.html", menu_items=bakery)


@app.route("/breakfast")
def breakfast():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_BREAKFAST)
            breakfast = cursor.fetchall()
            cursor.close()
    return render_template("breakfast.html", menu_items=breakfast)


@app.route("/lunch")
def lunch():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_LUNCH)
            lunch = cursor.fetchall()
            cursor.close()
    return render_template("lunch.html", menu_items=lunch)


@app.route("/dinner")
def dinner():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_DINNER)
            dinner = cursor.fetchall()
            cursor.close()
    return render_template("dinner.html", menu_items=dinner)


@app.route("/dessert")
def dessert():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_DESSERT)
            dessert = cursor.fetchall()
            cursor.close()
    return render_template("dessert.html", menu_items=dessert)


'''Begin API Functionality'''


#  Lunch and dinner
@app.route("/api/menuitems", methods=["POST"])
def create_menuitem():
    data = request.get_json()
    name = data["name"]
    description = data["description"]
    tag = data["tag"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_MENUITEM_RETURN_ID, (name, description, tag))
            id = cursor.fetchone()[0]
    return {"id": id, "name": name, "message": f"menu item {name} created."}, 201


@app.route("/api/menuitems", methods=["GET"])
def get_all_users():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_ITEMS)
            menu_items = cursor.fetchall()
            if menu_items:
                result = []
                for item in menu_items:
                    result.append({"id": item[0], "name": item[1], "description": item[2], "tag": item[3]})
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


# 404 handler

@app.errorhandler(404)
# inbuilt function which takes error as parameter
def not_found(e):
    # defining function
    return render_template("404.html")


if __name__ == "__main__":
    app.run()

# Have menu pop up with QR reader
# url is https://fluffy-cat-bb1787883c94.herokuapp.com/
