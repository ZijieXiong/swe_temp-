"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""

import json
import os

SWE_HOME = os.environ["SWE_HOME"]
TEST_MODE = os.environ.get("TEST_MODE", 0)

if TEST_MODE:
    DB_DIR = f"{SWE_HOME}/db/test_dbs"
else:
    DB_DIR = f"{SWE_HOME}/db"

FOOD_MENU_DB = f"{DB_DIR}/food_menu.json"
ROOMS_DB = f"{DB_DIR}/rooms.json"

def fetch_pets():
    """
    A function to return all pets in the data store.
    """
    return {"tigers": 2, "lions": 3, "zebras": 1}


def get_rooms():
    """
    A function to return all chat rooms
    """
    try:
        with open(ROOMS_DB) as file:
            return json.loads(file.read())
    except FileNotFoundError:
        return None


def get_food_menu():
    """
    A function to return food menu stored in data base
    """
    try:
        with open(FOOD_MENU_DB) as file:
            return json.loads(file.read())
    except FileNotFoundError:
        return None
