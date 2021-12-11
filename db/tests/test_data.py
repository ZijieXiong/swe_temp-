"""
This file holds the tests for db.py.
"""


from unittest import TestCase, skip

import db.db as db

def test_get_food_menu(self):
        """
        Can we fetch user db?
        """
        menu = db.get_food_menu()
        self.assertIsInstance(menu, dict)
def test_get_drink_menu(self):
        """
        Can we fetch user db?
        """
        menu = db.get_drink_menu()
        self.assertIsInstance(menu, dict)