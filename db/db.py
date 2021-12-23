"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""
import json
import os

import db.db_connect as dbc

SWE_HOME = os.environ["SWE_HOME"]
TEST_MODE = os.environ.get("TEST_MODE", 0)

DB_DIR = f"{SWE_HOME}/db"
FOOD_MENU_DB = f"{DB_DIR}/food_menu.json"
DRINK_MENU_DB = f"{DB_DIR}/drink_menu.json"
ROOMS_DB = f"{DB_DIR}/rooms.json"

FOOD_MENU = "foodMenu"
ROOMS = "rooms"
DRINK_MENU = "drinkMenu"
RESERVE = "reservation"

ROOM_NM = "roomName"
RESERVE_USER = "userName"
TIME = "time"
NUM_OF_PEOPLE = "numOfPeople"

OK = 0
NOT_FOUND = 1
DUPLICATE = 2

dbc.client = dbc.get_client()
if dbc.client is None:
    print("Failed to connect to MongoDB.")
    exit(1)
else:
    print("Successfully connect to MongoDB.")


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
    return dbc.fetch_all(ROOMS, ROOM_NM)


def get_reserve():
    """
    A function to return all reservations
    """
    return dbc.fetch_all_id(RESERVE)


def reserve_exists(userName, time, numOfUsers):
    """
    See if a reservation already exists in a db.
    Return True or False
    """
    rec = dbc.fetch_one(
        RESERVE,
        filters={RESERVE_USER: userName, TIME: time,
                 NUM_OF_PEOPLE: numOfUsers})
    print(f"{rec=}")
    return rec is not None


def add_reserve(userName, time, numOfUsers):
    """
    Add a reservation record to the reservation db.
    """
    print(f"{userName=}")
    if reserve_exists(userName, time, numOfUsers):
        return DUPLICATE
    else:
        dbc.insert_doc(RESERVE,
                       {RESERVE_USER: userName, TIME: time,
                        NUM_OF_PEOPLE: numOfUsers})
        return OK


def get_food_menu():
    """
    A function to return food menu stored in data base
    """
    return read_collection(FOOD_MENU_DB)


def get_drink_menu():
    """
    A function to return drink menu stored in data base
    """
    return read_collection(DRINK_MENU_DB)

"""
def get_soup_of_the_day(perm_version):
    "A function to return the soup of the day"

    "Iterate through soup of the day file"
    try:
        with open(perm_version) as f:
            file_read = json.load(f)
            for i in file_read['Soup of the day']['Friday']:
                print(i)
    except FileNotFoundError:
        print(f"{perm_version} not found.")
        return None
"""
