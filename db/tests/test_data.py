"""
This file holds the tests for db.py.
"""


from os import POSIX_FADV_SEQUENTIAL
from unittest import TestCase, skip

import db.db as db

class DBTestCase(TestCase):
        def setUp(self):
            POSIX_FADV_SEQUENTIAL

        def tearDown(self):
            pass

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
            user = db.get_user("zx811")
            self.assertTrue(user["password"] == "ForzaMilano")

        def test_user_exists1(self):
            """
            Test if we can check if a user really exists
            """
            self.assertTrue(db.user_exists("zx811"))

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
        """
        def test_get_soup(self):

                #Fetching soup options from db

                menu = db.get_soup_of_the_day()
                self.assertIsInstance(menu, dict)
        """
          
        def test_reserve_exists1(self):
            """
            Test if we can check if a reservation record really exists
            """
            self.assertTrue(db.reserve_exists('Tom', '2021-12-19 00:35:33.134848', 1))

        def test_reserve_exists2(self):
            """
            Test if we can check if a reservation record does not exists
            """
            self.assertFalse(db.reserve_exists('Sam', '2021-12-19 00:35:33.134848', 1))

        def test_food_exists(self):
                """
                Test if a specific food item entry in the food db actually exists
                """
                self.assertTrue(db.food_item_exists('Pancake'))


