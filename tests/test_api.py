import json
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


# Retrieving menu items should return a 200
def test_apiget(client):
    apiget = client.get("/api/menuitems")
    assert apiget.status_code == 200


# Invalid menu item to delete returns 404
def test_api_delete_fail(client):
    api_delete = client.delete("/api/menuitems/1000")
    assert api_delete.status_code == 404


# Put request returns 200
def test_api_put_price(client):
    put_url = "api/menuitems/11"
    data = {
        "price": "$0.01"
    }

    put_url = client.put(put_url, data=json.dumps(data), content_type='application/json')
    assert put_url.status_code == 200


# Post request returns 201
def test_api_create(client):
    create_url = "/api/menuitems"
    data = {
        "name": "test",
        "description": "description test",
        "tag": "test tag",
        "price": "$1.00"
    }

    put_url = client.post(create_url, data=json.dumps(data), content_type='application/json')
    assert put_url.status_code == 201
