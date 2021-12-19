"""
This file holds the tests for endpoints.py
"""

from unittest import TestCase, skip
from flask_restx import Resource, Api
import API.endpoints as ep

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

