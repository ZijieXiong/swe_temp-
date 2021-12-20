"""
This file holds the tests for endpoints.py
"""

from unittest import TestCase, skip
from flask_restx import Resource, Api
import API.endpoints as ep
import db.db as db
import random

HUGE_NUM = 100000000000

def new_entity_name(entity_type):
    int_name = random.randint(0, HUGE_NUM)
    return f"new {entity_type}" + str(int_name)

class EndpointTestCase(TestCase):
    def setUp(self):
        pass;

    def tearDown(self):
        pass;

    def test_hello(self):
        hello = ep.HelloWorld(Resource)
        ret = hello.get()
        self.assertIsInstance(ret, dict)
        self.assertIn(ep.HELLO, ret)

    def test_food_menu1(self):
        """
        Post-condition 1: return is a dictionary
        """
        fm = ep.ListFoodMenu(Resource)
        ret = fm.get()
        self.assertIsInstance(ret, dict)
    
    def test_food_menu2(self):
        """
        Post-condition 2: keys to the dictionary are strings
        """
        fm = ep.ListFoodMenu(Resource)
        ret = fm.get()
        for key in ret:
            self.assertIsInstance(key, str)
    
    def test_food_menu3(self):
        """
        Post-condition 3: values in the dict are dicts too.
        """
        fm = ep.ListFoodMenu(Resource)
        ret = fm.get()
        for val in ret.values():
            self.assertIsInstance(val, dict)

    def test_list_reservation1(self):
        """
        Post-condition 1: return is a dictionary
        """
        fm = ep.ListReservation(Resource)
        ret = fm.get()
        self.assertIsInstance(ret, dict)
    
    def test_list_reservation(self):
        """
        Post-condition 2: values in dicts are dict too
        """
        fm = ep.ListReservation(Resource)
        ret = fm.get()
        for val in ret.values():
            self.assertIsInstance(val, dict)

    def test_add_reservation(self):
        """
        Test if we can successfully create a new reservation.
        """
        cr = ep.CreateReserve(Resource)
        new_reserve = new_entity_name("reserve")
        ret = cr.post(new_reserve, "2021-12-19 00:35:33.134848", 1)
        print(f"{ret=}")
        self.assertTrue(db.reserve_exists(new_reserve, "2021-12-19 00:35:33.134848", 1))


