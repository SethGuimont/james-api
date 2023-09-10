import pytest
from app import *


@pytest.fixture
def client():
    """Configures the app for testing

    Sets app config variable ``TESTING`` to ``True``

    :return: App for testing
    """

    # app.config['TESTING'] = True
    client = app.test_client()

    yield client


def test_landing(client):
    landing = client.get("/")
    html = landing.data.decode()

    assert "Fluffy Cat Pizza" in html
    assert landing.status_code == 200


def test_bakery(client):
    bakery_page = client.get("/bakery")
    html = bakery_page.data.decode()

    assert "Bakery" in html
    assert bakery_page.status_code == 200


def test_breakfast(client):
    breakfast_page = client.get("/breakfast")
    html = breakfast_page.data.decode()

    assert "Breakfast" in html
    assert breakfast_page.status_code == 200


def test_lunch(client):
    lunch_page = client.get("/lunch")
    html = lunch_page.data.decode()

    assert "Lunch" in html
    assert lunch_page.status_code == 200


def test_dinner(client):
    dinner_page = client.get("/dinner")
    html = dinner_page.data.decode()

    assert "Dinner" in html
    assert dinner_page.status_code == 200


def test_dessert(client):
    dessert_page = client.get("/dessert")
    html = dessert_page.data.decode()

    assert "Dessert" in html
    assert dessert_page.status_code == 200


def test_apiget(client):
    apiget = client.get("/api/menuitems")
    assert apiget.status_code == 200
