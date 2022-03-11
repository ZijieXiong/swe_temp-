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
DRINK_NAME = "drinkName"
PRICE = "price"
TYPE = "type"

OK = 0
NOT_FOUND = 1
DUPLICATE = 2
DRINK_TYPE = ["Alcoholic", "Non alcoholic", "Juice"]

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


def update_reserve(userName, time, new_time="", numOfUsers=-1):
    """
    Update a reservation record from the reservation db
    """
    if reserve_exists(userName, time):
        dbc.update_one(
            RESERVE,
            {USER_NAME: userName, TIME: time},
            {
                "$set": {TIME: new_time, NUM_OF_PEOPLE: numOfUsers},
                "$currentDate": {"LastModified": True}
            }
            )
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


def update_food_item(foodName, new_foodName=""):
    """
    Change the name of a food item in food_menu db
    """
    if food_item_exists(foodName):
        dbc.update_one(
            FOOD_MENU,
            {FOOD_NAME: foodName},
            {
                "$set": {FOOD_NAME: new_foodName}
            }
            )
        return OK
    else:
        return NOT_FOUND


def get_food_menu():
    """
    Function to return the food menu within the mongo database
    """
    return dbc.fetch_all_id(FOOD_MENU)


def drink_item_exists(drinkName):
    """
    A function that checks if a drink item exists in the drink menu db
    """
    rec = dbc.fetch_one(DRINK_MENU,
                        filters={DRINK_NAME: drinkName})
    return rec is not None


def add_drink_item(drinkName):
    """
    A function that attempts to add a drink item to the drink db
    """
    if drink_item_exists(drinkName):
        return DUPLICATE
    else:
        dbc.insert_doc(DRINK_MENU,
                       {DRINK_NAME: drinkName})
        return OK


def delete_drink_item(drinkName):
    """
    Attempts to delete a drink item from drink_menu db
    """
    if drink_item_exists(drinkName):
        dbc.del_one(DRINK_MENU,
                    {DRINK_NAME: drinkName})
        return OK
    else:
        return NOT_FOUND


def update_drink_item(drinkName, new_drinkName=""):
    """
    Change the name of a food item in food_menu db
    """
    if drink_item_exists(drinkName):
        dbc.update_one(
            DRINK_MENU,
            {DRINK_NAME: drinkName},
            {
                "$set": {DRINK_NAME: new_drinkName}
            }
            )
        return OK
    else:
        return NOT_FOUND


def get_drink_menu():
    """
    A function to return drink menu stored in data base
    """
    drink_menu = {}
    for drinkType in DRINK_TYPE:
        drink_menu[drinkType] = dbc.fetch_all(
            DRINK_MENU,
            DRINK_NAME,
            {
                TYPE: drinkType
            }
        )
    return drink_menu
