import pytest
import requests
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


# Retrieving menu items should return a 200
def test_apiget(client):
    apiget = client.get("/api/menuitems")
    assert apiget.status_code == 200


# Invalid menu item to delete returns 404
def test_api_delete(client):
    api_delete = client.delete("/api/menuitems/1000")
    assert api_delete.status_code == 404


# Fix later
def test_create_new_user():
    put_url = "https://fluffy-cat-bb1787883c94.herokuapp.com/api/menuitems/13"
    data = {
        "price": "$1.00"
    }

    response = requests.put(put_url, data=data)
    assert response.status_code == 415
