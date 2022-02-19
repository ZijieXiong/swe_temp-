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

USER = "users"

FOOD_MENU = "foodMenu"
ROOMS = "rooms"
DRINK_MENU = "drinkMenu"
RESERVE = "reservation"

USER_NAME = "userName"
PASSWORD = "password"
USER_TYPE = "type"


ROOM_NM = "roomName"
TIME = "time"
NUM_OF_PEOPLE = "numOfPeople"

FOOD_NAME = "foodName"
PRICE = "price"

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


def get_users():
    """
    A function to return all users
    """
    return dbc.fetch_all(USER, USER_NAME)


def get_user(userName):
    """
    A function to return one user with the user name
    """
    return dbc.fetch_one(
        USER, filters={USER_NAME: userName})


def user_exists(userName):
    """
    See if a user already exists in a db.
    Return True or False
    """
    rec = dbc.fetch_one(
        USER,
        filters={USER_NAME: userName})
    return rec is not None


def add_user(userName, password, type):
    """
    Add a user record to the users db
    """
    if(user_exists(userName)):
        return DUPLICATE
    else:
        dbc.insert_doc(
            USER,
            {USER_NAME: userName,
             PASSWORD: password,
             USER_TYPE: type})
        return OK


def delete_user(userName):
    """
    Deletes a user record from the users db
    """
    if(user_exists(userName)):
        dbc.del_one(USER,
                    {USER_NAME: userName})
        return OK
    else:
        return NOT_FOUND


def get_reserve():
    """
    A function to return all reservations
    """
    return dbc.fetch_all_id(RESERVE)


def reserve_exists(userName, time):
    """
    See if a reservation already exists in a db.
    Return True or False
    """
    rec = dbc.fetch_one(
        RESERVE,
        filters={USER_NAME: userName, TIME: time})
    return rec is not None


def add_reserve(userName, time, numOfUsers):
    """
    Add a reservation record to the reservation db.
    """
    if reserve_exists(userName, time):
        return DUPLICATE
    else:
        dbc.insert_doc(RESERVE,
                       {USER_NAME: userName, TIME: time,
                        NUM_OF_PEOPLE: numOfUsers})
        return OK


def delete_reserve(userName, time):
    """
    Delete a reservation record from the reservation db.
    """
    if reserve_exists(userName, time):
        dbc.del_one(RESERVE,
                    {USER_NAME: userName, TIME: time})
        return OK
    else:
        return NOT_FOUND


def food_item_exists(foodName):
    """
    See if a specific food item already exists in db
    """
    rec = dbc.fetch_one(
            FOOD_MENU,
            filters={FOOD_NAME: foodName})
    return rec is not None


def add_food_item(foodName):
    """
    Add a food item to the food_menu db
    """
    if food_item_exists(foodName):
        return DUPLICATE
    else:
        dbc.insert_doc(FOOD_MENU,
                       {FOOD_NAME: foodName})
        return OK


def delete_food_item(foodName):
    """
    Deletes a food item from the food_menu db
    """
    if food_item_exists(foodName):
        dbc.del_one(FOOD_MENU,
                    {FOOD_NAME: foodName})
        return OK
    else:
        return NOT_FOUND


def get_food():
    """
    Function to return the food menu within the mongo database
    """
    return dbc.fetch_all_id(FOOD_MENU)


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
