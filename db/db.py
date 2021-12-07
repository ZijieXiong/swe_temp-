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



def read_collection(perm_version):
    """
    A function to read a colleciton off of disk.
    """
    try:
        with open(perm_version) as file:
            return json.loads(file.read())
    except FileNotFoundError:
        print(f"{perm_version} not found.")
        return None


def get_rooms():
    """
    A function to return all chat rooms
    """
    return read_collection(ROOMS_DB)


def get_food_menu():
    """
    A function to return food menu stored in data base
    """
    return read_collection(FOOD_MENU_DB)
