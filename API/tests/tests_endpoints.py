"""
This file holds the tests for endpoints.py
"""

import string
from tokenize import String
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

    def test_log_in1(self):
        """
        Test if we can login with valid account and password
        """
        li = ep.LogIn(Resource)
        ret = li.post("zx811", "ForzaMilano")
        self.assertIsInstance(ret, int)

    def test_log_in2(self):
        """
        Test if we can login with invalid account
        """
        li = ep.LogIn(Resource)
        ret = li.post("", "123")
        self.assertTrue(ret == 0)

    def test_log_in3(self):
        """
        Test if we can login with a valid account and a invalid password
        """    
        li = ep.LogIn(Resource)
        ret = li.post("zx811", "")
        self.assertTrue(ret == 0)

    def test_register_user(self):
        """
        Test if we can register a new user with unduplicated username
        """
        rg = ep.RegisterUser(Resource)
        new_user = new_entity_name("user")
        ret = rg.post(new_user, "123456", 1)
        self.assertTrue(db.user_exists(new_user))
    
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
        self.assertTrue(db.reserve_exists(new_reserve, "2021-12-19 00:35:33.134848"))

    def test_del_rserveation(self):
        """
        Test if we can successfully delete an existed reservation.
        """
        cr = ep.CreateReserve(Resource)
        new_reserve = new_entity_name("reserve")
        time = "2021-12-19 00:35:33.134848"
        cr.post(new_reserve, "2021-12-19 00:35:33.134848", 1)
        dr = ep.DeleteReserve(Resource)
        ret = dr.post(new_reserve, "2021-12-19 00:35:33.134848")
        self.assertIsInstance(ret, str)
        

    def test_add_food_item(self):
        """
        Test if we can successfully add/create a new food item
        """
        fi = ep.NewFoodItem(Resource)
        new_food_item = new_entity_name("food_name")
        ret = fi.post(new_food_item)
        self.assertTrue(db.food_item_exists(new_food_item))
    

    def test_add_drink_item(self):
        """
        Test if we can successfully add/create a new drink item
        """
        di = ep.NewDrinkItem(Resource)
        new_drink_item = new_entity_name("drink_name")
        ret = di.post(new_drink_item)
        self.assertTrue(db.drink_item_exists(new_drink_item))

    """
    In Progress
    def test_delete_food_item(self):
        Test if we can successfully delete a food item after adding a food item
        fi = ep.NewFoodItem(Resource)
        new_food_item = new_entity_name("food_name")
        ret = fi.post(new_food_item)
        self.assertTrue(db.food_item_exists(new_food_item))

        dl = ep.DeleteFoodItem(new_food_item)
        self.assertFalse(db.food_item_exists(new_food_item))
    """
