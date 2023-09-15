import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template, session, flash, redirect, abort
from flask_cors import CORS
from constants import *
import stripe

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(12)
CORS(app)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
stripe_pup = os.getenv("STRIPE_PUP_KEY")

YOUR_DOMAIN = 'http://127.0.0.1:5000'

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
            menu_items = cursor.fetchall()
            cursor.close()
    return render_template("bakery.html", menu_items=menu_items)


@app.route("/breakfast")
def breakfast():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_BREAKFAST)
            menu_items = cursor.fetchall()
            cursor.close()
    return render_template("breakfast.html", menu_items=menu_items)


@app.route("/lunch")
def lunch():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_LUNCH)
            menu_items = cursor.fetchall()
            cursor.close()
    return render_template("lunch.html", menu_items=menu_items)


@app.route("/dinner")
def dinner():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_DINNER)
            menu_items = cursor.fetchall()
            cursor.close()
    return render_template("dinner.html", menu_items=menu_items)


@app.route("/dessert")
def dessert():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_DESSERT)
            menu_items = cursor.fetchall()
            cursor.close()
    return render_template("dessert.html", menu_items=menu_items)


# Admin Portal Pages and Login
@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return employee()


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return employee()


@app.route("/employee")
def employee():
    if not session.get('logged_in'):
        return render_template("login.html")
    else:
        return render_template("employee.html")


# payment handler
@app.route("/payment")
def payment():
    return render_template("payment.html")


@app.route("/success")
def success():
    return render_template("success.html")


@app.route("/cancelled")
def cancelled():
    return render_template("cancelled.html")


@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1Nqi1mD2IPz5VDJsARJppQP7',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success',
            cancel_url=YOUR_DOMAIN + '/cancelled',
        )
    except Exception as e:
        return str(e)
    return redirect(checkout_session.url, code=303)


'''Begin API Functionality'''


@app.route("/api/menuitems", methods=["POST"])
def create_menuitem():
    data = request.get_json()
    name = data["name"]
    description = data["description"]
    tag = data["tag"]
    price = data["price"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_MENUITEM_RETURN_ID, (name, description, tag, price))
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
                    result.append(
                        {"id": item[0], "name": item[1], "description": item[2], "tag": item[3], "price": item[4]})
                return jsonify(result)
            else:
                return jsonify({"error": f"Users not found."}), 404


@app.route("/api/menuitems/<int:id>", methods=["PUT"])
def update_menuitem_price(id):
    data = request.get_json()
    price = data["price"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_MENUITEM_PRICE, (price, id))
            if cursor.rowcount == 0:
                return jsonify({"error": f"Menu item with ID {id} not found."}), 404
            return jsonify({"id": id, "price": price, "message": f"Menu Item with ID {id} updated."})


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


# Payment handler


if __name__ == "__main__":
    app.run()

# Have menu pop up with QR reader
# url is https://fluffy-cat-bb1787883c94.herokuapp.com/
