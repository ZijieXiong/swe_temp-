"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""
from http.client import NOT_ACCEPTABLE
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
ORDERS = "orders"

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

FOOD_TYPE = 'foodType'
DRINK_TYPE = 'drinkType'

ITEMS = "items"
FOOD = "food"
DRINKS = "drinks"
DESCRIPTION = "description"
POPULARITY = "popularity"
QUANTITY = "quantity"
COST = "cost"
ORDER_TYPE = "orderType"
ORDER_NUMBER = "orderNumber"
ORDER_NUM = 0

FEEDBACK_LIST = "feedbackList"
FEEDBACK = "feedback"

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


def get_one_food_item(foodName):
    """
    Get a specific food item in db
    """
    rec = dbc.fetch_one(
        FOOD_MENU,
        filters={FOOD_NAME: foodName})
    return rec


def add_food_item(foodName, food_type, price, description):
    """
    Add a food item to the food_menu db
    """
    if food_item_exists(foodName):
        return DUPLICATE
    else:
        popularity = 0
        dbc.insert_doc(FOOD_MENU,
                       {
                            FOOD_NAME: foodName,
                            TYPE: food_type,
                            PRICE: price,
                            DESCRIPTION: description,
                            POPULARITY: popularity
                       })
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


def update_food_item(foodName, new_foodName, new_foodType,
                     new_price, new_description, new_pop=-1):
    """
    Change the name of a food item in food_menu db
    """
    if food_item_exists(foodName):
        new_data = {}
        if(new_foodName is not None):
            new_data[FOOD_NAME] = new_foodName
        if(new_foodType is not None):
            new_data[TYPE] = new_foodType
        if(new_price is not None):
            new_data[PRICE] = new_price
        if(new_description is not None):
            new_data[DESCRIPTION] = new_description
        if(new_pop != -1):
            new_data[POPULARITY] = new_pop
        dbc.update_one(
            FOOD_MENU,
            {FOOD_NAME: foodName},
            {
                "$set": new_data
            }
            )
        return OK


def get_food_menu():
    """
    Function to return the food menu stored in data base
    """
    food_menu = {}
    food_types = get_food_type()
    for value in food_types.values():
        food_menu[value["typeName"]] = dbc.fetch_all(
            FOOD_MENU,
            FOOD_NAME,
            {
                    TYPE: value["typeName"]
            }
        )
    return food_menu


def get_food_type():
    """
    Function to return food type stored in database
    """
    return dbc.fetch_all_id(FOOD_TYPE)


def drink_item_exists(drinkName):
    """
    A function that checks if a drink item exists in the drink menu db
    """
    rec = dbc.fetch_one(DRINK_MENU,
                        filters={DRINK_NAME: drinkName})
    return rec is not None


def get_one_drink_item(drinkName):
    """
    A function to return a specific drink item in db based on drinkName.
    """
    rec = dbc.fetch_one(DRINK_MENU,
                        filters={DRINK_NAME: drinkName})
    return rec


def add_drink_item(drinkName, drink_type, price, description):
    """
    A function that attempts to add a drink item to the drink db
    """
    if drink_item_exists(drinkName):
        return DUPLICATE
    else:
        popularity = 0
        dbc.insert_doc(DRINK_MENU,
                       {
                           DRINK_NAME: drinkName,
                           TYPE: drink_type,
                           PRICE: price,
                           DESCRIPTION: description,
                           POPULARITY: popularity
                       })
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


def update_drink_item(drinkName, new_drinkName, new_drinkType,
                      new_price, new_description, new_pop=-1):
    """
    Change the name of a food item in food_menu db
    """
    if drink_item_exists(drinkName):
        new_data = {}
        if(new_drinkName is not None):
            new_data[DRINK_NAME] = new_drinkName
        if(new_drinkType is not None):
            new_data[TYPE] = new_drinkType
        if(new_price is not None):
            new_data[PRICE] = new_price
        if(new_description is not None):
            new_data[DESCRIPTION] = new_description
        if(new_pop != -1):
            new_data[POPULARITY] = new_pop
        dbc.update_one(
            DRINK_MENU,
            {DRINK_NAME: drinkName},
            {
                "$set": new_data
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
    drink_types = get_drink_type()
    for value in drink_types.values():
        drink_menu[value["typeName"]] = dbc.fetch_all(
            DRINK_MENU,
            DRINK_NAME,
            {
                TYPE: value["typeName"]
            }
        )
    return drink_menu


def get_drink_type():
    """
    A function to return drink type stored in data base
    """
    return dbc.fetch_all_id(DRINK_TYPE)


def add_order(userName, foodName, drinkName,
              foodQuanti, drinkQuanti, orderType):
    """
    A function to add a new order into the order db.
    """
    items = {}
    food = {}
    drinks = {}
    cost = 0
    global ORDER_NUM
    ORDER_NUM = ORDER_NUM + 1
    orderNumber = ORDER_NUM
    if(foodName is not None or foodQuanti is not None):
        if(len(foodName) != len(foodQuanti)):
            return NOT_ACCEPTABLE
        for i in range(len(foodName)):
            if(food_item_exists(foodName[i])):
                food_item = get_one_food_item(foodName[i])
                update_food_item(
                    foodName[i], None, None, food_item[POPULARITY]+1)
                food[foodName[i]] = {
                    FOOD_NAME: foodName[i],
                    QUANTITY: foodQuanti[i],
                    COST: food_item[PRICE]*foodQuanti[i]
                    }
                cost += food_item[PRICE]*foodQuanti[i]
            else:
                return NOT_FOUND
    if(drinkName is not None or drinkQuanti is not None):
        if(len(drinkName) != len(drinkQuanti)):
            return NOT_ACCEPTABLE
        for i in range(len(drinkName)):
            if(drink_item_exists(drinkName[i])):
                drink_item = get_one_drink_item(drinkName[i])
                drinks[drinkName[i]] = {
                    DRINK_NAME: drinkName[i],
                    QUANTITY: drinkQuanti[i],
                    COST: drink_item[PRICE]*drinkQuanti[i]
                    }
                cost += drink_item[PRICE]*drinkQuanti[i]
            else:
                return NOT_FOUND
    items[FOOD] = food
    items[DRINKS] = drinks
    dbc.insert_doc(
            ORDERS,
            {
                USER_NAME: userName,
                ITEMS: items,
                COST: cost,
                ORDER_TYPE: orderType,
                ORDER_NUMBER: orderNumber
            })
    return OK


def get_order_list():
    return dbc.fetch_all_id(ORDERS)


def order_exists(orderNumber):
    """
    Check if an order exists via order number
    """
    rec = dbc.fetch_one(ORDERS,
                        filters={ORDER_NUMBER: orderNumber})
    return rec is not None


def get_order(orderNumber):
    """
    A function to return a specific order/details of an order
    """
    rec = dbc.fetch_one(ORDERS,
                        filters={ORDER_NUMBER: orderNumber})
    return rec


def get_order_by_user(userName):
    """
    A function to return the oders of a specifc user.
    """
    rec = dbc.fetch_all_id(ORDERS, filters={USER_NAME: userName})
    return rec


def delete_order(orderNumber):
    """
    Attempts to delete a specific order from order db
    """
    if order_exists(orderNumber):
        dbc.del_one(ORDERS,
                    {ORDER_NUMBER: orderNumber})
        return OK
    else:
        return NOT_FOUND


def add_feedback(feedback):
    """
    This function attempts to add a string to feedback db
    """
    dbc.insert_doc(FEEDBACK_LIST,
                   {
                       FEEDBACK: feedback
                   })
    return OK
