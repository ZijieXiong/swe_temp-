"""
This file holds the tests for db.py.
"""


from os import POSIX_FADV_SEQUENTIAL
from unittest import TestCase, skip

import db.db as db
from db.db_connect import client, db_nm
import random

KNOWN_USER_NM = "Known user"
KNOWN_USER_PW = "123456"
KNOWN_USER_TYPE = 1
KNOWN_RESERV_TIME = "2021-12-19 00:35:33.134848"
KNOWN_RESERV_NUM = 1

HUGE_NUM = 100000000000

def new_entity_name(entity_type):
    int_name = random.randint(0, HUGE_NUM)
    return f"new {entity_type}" + str(int_name)

class DBTestCase(TestCase):
        def setUp(self):
            POSIX_FADV_SEQUENTIAL
            client[db_nm][db.USER].insert_one({db.USER_NAME: KNOWN_USER_NM, db.PASSWORD: KNOWN_USER_PW, db.USER_TYPE: KNOWN_USER_TYPE})
            client[db_nm][db.RESERVE].insert_one({db.USER_NAME: KNOWN_USER_NM, db.TIME: KNOWN_RESERV_TIME, db.NUM_OF_PEOPLE: KNOWN_RESERV_NUM})

        def tearDown(self):
            pass;

        def test_get_users(self):
            """
            Can we fetch user db?
            """
            users = db.get_users()
            self.assertIsInstance(users, dict)

        def test_get_user(self):
            """
            Can we fetch one specific user?
            """
            user = db.get_user(KNOWN_USER_NM)
            self.assertTrue(user[db.PASSWORD] == KNOWN_USER_PW)

        def test_user_exists1(self):
            """
            Test if we can check if a user really exists
            """
            self.assertTrue(db.user_exists(KNOWN_USER_NM))

        def test_user_exists2(self):
            """
            Test if we can check if a user does not exists
            """
            self.assertFalse(db.user_exists("__"))

        def test_get_food_menu(self):
            """
            Can we fetch food menu?
            """
            menu = db.get_food_menu()
            self.assertIsInstance(menu, dict)
                
        def test_get_drink_menu(self):
            """
            Can we fetch user db?
            """
            menu = db.get_drink_menu()
            self.assertIsInstance(menu, dict)
          
        def test_reserve_exists1(self):
            """
            Test if we can check if a reservation record really exists
            """
            self.assertTrue(db.reserve_exists(KNOWN_USER_NM, KNOWN_RESERV_TIME))

        def test_reserve_exists2(self):
            """
            Test if we can check if a reservation record does not exists
            """
            self.assertFalse(db.reserve_exists('Sam', '2021-12-19 00:35:33.134848'))

        def test_update_reserve(self):
            """
            Test if we can successfully update a reservation record
            """
            self.assertFalse(db.update_reserve(KNOWN_USER_NM, KNOWN_RESERV_TIME, KNOWN_RESERV_TIME+"1", 2))


