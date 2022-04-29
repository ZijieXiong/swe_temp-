"""
This file holds the tests for endpoints.py
"""

import string
from tokenize import String
from unittest import TestCase, skip
from flask_restx import Resource, Api
import API.endpoints as ep
import db.db as db
from db.db_connect import client, db_nm
import random

HUGE_NUM = 100000000000
KNOWN_USER_NM = "Known user"
KNOWN_USER_PW = "123456"
KNOWN_USER_TYPE = 1

KNOWN_DRINK_NAME = "Corona"
KNOWN_DRINK_TYPE = "Beer"
KNOWN_FOOD_NAME = "Fries"
KNOWN_FOOD_TYPE = "Appetizer"
KNOWN_DES = "placeholder"
KNOWN_PRICE = 1

KNOWN_RESERV_TIME = "2021-12-19 00:35"
KNOWN_RESERV_NUM = 1

def new_entity_name(entity_type):
    int_name = random.randint(0, HUGE_NUM)
    return f"new {entity_type}" + str(int_name)

class EndpointTestCase(TestCase):
    def setUp(self):
        client[db_nm][db.USER].insert_one({db.USER_NAME: KNOWN_USER_NM, db.PASSWORD: KNOWN_USER_PW, db.USER_TYPE: KNOWN_USER_TYPE})
        client[db_nm][db.DRINK_TYPE].insert_one({db.TYPE_NAME: KNOWN_DRINK_TYPE})
        client[db_nm][db.DRINK_MENU].insert_one({db.DRINK_NAME: KNOWN_DRINK_NAME, db.TYPE: KNOWN_DRINK_TYPE, db.PRICE: KNOWN_PRICE, db.DESCRIPTION: KNOWN_DES, db.POPULARITY: 0})
        client[db_nm][db.FOOD_TYPE].insert_one({db.TYPE_NAME: KNOWN_FOOD_TYPE})
        client[db_nm][db.FOOD_MENU].insert_one({db.FOOD_NAME: KNOWN_FOOD_NAME, db.TYPE: KNOWN_FOOD_TYPE, db.PRICE: KNOWN_PRICE, db.DESCRIPTION: KNOWN_DES, db.POPULARITY: 0})
        client[db_nm][db.RESERVE].insert_one({db.USER_NAME: KNOWN_USER_NM, db.TIME: KNOWN_RESERV_TIME, db.NUM_OF_PEOPLE: KNOWN_RESERV_NUM})

    def tearDown(self):
        client[db_nm][db.USER].delete_many({})
        client[db_nm][db.DRINK_TYPE].delete_many({})
        client[db_nm][db.DRINK_MENU].delete_many({})
        client[db_nm][db.FOOD_MENU].delete_many({})
        client[db_nm][db.FOOD_TYPE].delete_many({})
        client[db_nm][db.RESERVE].delete_many({})
        client[db_nm][db.REVIEW_LIST].delete_many({})

    def test_log_in1(self):
        """
        Test if we can login with valid account and password
        """
        li = ep.LogIn(Resource)
        ret = li.post(KNOWN_USER_NM, KNOWN_USER_PW)
        self.assertTrue(ret == 1)

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

    def test_drink_type(self):
        """
        Post-condition 1: returned value is a dict
        """
        dt = ep.ListDrinkType(Resource)
        ret = dt.get()
        self.assertIsInstance(ret, dict)

    def test_drink_type2(self):
        """
        Post-condition 2: value in the returned value is dict too
        """
        dt = ep.ListDrinkType(Resource)
        ret = dt.get()
        for val in ret.values():
            self.assertIsInstance(val, dict)

    def test_drink_menu1(self):
        """
        Post-condition 1: return value is a dict.
        """
        dm = ep.ListDrinkMenu(Resource)
        ret = dm.get()
        self.assertIsInstance(ret, dict)

    def test_drink_menu2(self):
        """
        Post-condition 2: values in the dict are dicts too.
        """
        dm = ep.ListDrinkMenu(Resource)
        ret = dm.get()
        for val in ret.values():
            self.assertIsInstance(val, dict)

    def test_drink_menu3(self):
        """
        Post-condition 3: values in the dict inside the dict are dicts too.
        """
        dm = ep.ListDrinkMenu(Resource)
        ret = dm.get()
        for val1 in ret.values():
            for val2 in val1.values():
                self.assertIsInstance(val2, dict)

    def test_list_drink_by_type1(self):
        """
        Post-condition 1: return is a dictionary
        """
        ldbt = ep.ListDrinkByType(Resource)
        ret = ldbt.post(KNOWN_DRINK_TYPE)
        self.assertIsInstance(ret, dict)

    def test_list_dood_by_type2(self):
        """
        Post-condition 2: values is the dict are dicts too
        """
        ldbt = ep.ListFoodByType(Resource)
        ret = ldbt.post(KNOWN_DRINK_TYPE)
        for val in ret.values():
            self.assertIsInstance(val, dict)

    def test_add_drink_item(self):
        """
        Test if we can successfully add/create a new drink item
        """
        di = ep.NewDrinkItem(Resource)
        new_drink_item = new_entity_name("drink_name")
        drinkType = db.get_drink_type()
        ret = di.post(new_drink_item, list(drinkType.values())[0]["typeName"], 1, 'Placeholder text')
        self.assertTrue(db.drink_item_exists(new_drink_item))

    def test_delete_drink_item(self):
        """
        Test if we can successfully delete a drink item after adding a drink item
        """
        ddi = ep.DeleteDrinkItem(Resource)
        ret = ddi.post(KNOWN_DRINK_NAME)
        self.assertIsInstance(ret, str)

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
        ret = cr.post(new_reserve, KNOWN_RESERV_TIME, 1)
        self.assertTrue(db.reserve_exists(new_reserve, KNOWN_RESERV_TIME))

    def test_del_rserveation(self):
        """
        Test if we can successfully delete an existed reservation.
        """
        dr = ep.DeleteReserve(Resource)
        ret = dr.post(KNOWN_USER_NM, KNOWN_RESERV_TIME)
        self.assertIsInstance(ret, str)
        
    def test_food_type(self):
        """
        Post-condition 1: returned value is a dict
        """
        dt = ep.ListFoodType(Resource)
        ret = dt.get()
        self.assertIsInstance(ret, dict)

    def test_food_type2(self):
        """
        Post-condition 2: value in the returned value is dict too
        """
        dt = ep.ListFoodType(Resource)
        ret = dt.get()
        for val in ret.values():
            self.assertIsInstance(val, dict)

    def test_food_menu1(self):
        """
        Post-condition 1: return is a dictionary
        """
        fm = ep.ListFoodMenu(Resource)
        ret = fm.get()
        self.assertIsInstance(ret, dict)
   
    def test_food_menu2(self):
        """
        Post-condition 2: values in the dict are dicts too
        """
        fm = ep.ListFoodMenu(Resource)
        ret = fm.get()
        for val in ret.values():
            self.assertIsInstance(val, dict)
    
    def test_food_menu3(self):
        """
        Post-condition 3: values in the dict inside the dict are dicts too.
        """
        fm = ep.ListFoodMenu(Resource)
        ret = fm.get()
        for val1 in ret.values():
            for val2 in val1.values():
                self.assertIsInstance(val2, dict)

    def test_list_food_by_type1(self):
        """
        Post-condition 1: return is a dictionary
        """
        lfbt = ep.ListFoodByType(Resource)
        ret = lfbt.post(KNOWN_FOOD_TYPE)
        self.assertIsInstance(ret, dict)

    def test_list_food_by_type2(self):
        """
        Post-condition 2: values is the dict are dicts too
        """
        lfbt = ep.ListFoodByType(Resource)
        ret = lfbt.post(KNOWN_FOOD_TYPE)
        for val in ret.values():
            self.assertIsInstance(val, dict)

    def test_add_food_item(self):
        """
        Test if we can successfully add/create a new food item
        """
        fi = ep.NewFoodItem(Resource)
        new_food_item = new_entity_name("food_name")
        foodType = db.get_food_type()
        ret = fi.post(new_food_item, list(foodType.values())[0]["typeName"], 1, "Placeholder text")
        self.assertTrue(db.food_item_exists(new_food_item))
    
    def test_delete_food_item(self):
        """
        Test if we can successfully delete a food item after adding a food item
        """
        fi = ep.NewFoodItem(Resource)
        new_food_item = new_entity_name("food_name")
        foodType = db.get_food_type()
        ret = fi.post(new_food_item, list(foodType.values())[0]["typeName"], 1, "Delicious thing")
        dfi = ep.DeleteFoodItem(Resource)
        self.assertIsInstance(ret, str)

    def test_list_order1(self):
        """
        Post-condition 1: return value is a dict
        """
        lo = ep.ListOrder()
        ret = lo.get()
        self.assertIsInstance(ret, dict)
    
    def test_list_order2(self):
        """
        Post-condition 2: values in the dict are dicts too
        """
        lo = ep.ListOrder()
        ret = lo.get()
        for val in ret.values():
            self.assertIsInstance(val, dict)

    def test_list_order_by_user1(self):
        """
        Post-condition 1: return value is a dict
        """
        lobu = ep.ListOrderByUser()
        ret = lobu.post(KNOWN_USER_NM)
        self.assertIsInstance(ret, dict)

    def test_list_order_by_user2(self):
        lobu = ep.ListOrderByUser()
        ret = lobu.post(KNOWN_USER_NM)
        for val in ret.values():
            self.assertIsInstance(val, dict)

    def test_add_review(self):
        """
        Test if we can add a review
        """
        rv = ep.NewReview(Resource)
        new_review = new_entity_name("review")
        ret = rv.post(new_review)
        self.assertIsInstance(ret, str)
    
    def test_list_review1(self):
        """
        Post-condition 1: return value is a dict.
        """
        lr = ep.ListReviews()
        ret = lr.get()
        self.assertIsInstance(ret, dict)

    def test_list_review2(self):
        """
        Post-condition 2: values in dict are dicts too
        """
        lr = ep.ListReviews()
        ret = lr.get()
        for val in ret.values():
            self.assertIsInstance(ret, dict)