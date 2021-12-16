"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

from flask import Flask
from flask_restx import Resource, Api
import db.db as db


app = Flask(__name__)
api = Api(app)
HELLO = 'hello'


@api.route('/hello')
class HelloWorld(Resource):
    """
    The purpose of the HelloWorld class is to have a simple test to see if the
    app is working at all.
    """
    def get(self):
        """
        A trivial endpoint to see if the server is running.
        It just answers with "hello world."
        """
        return {HELLO: 'world'}


@api.route('/endpoints')
class Endpoints(Resource):
    """
    This class will serve as live, fetchable documentation of what endpoints
    are available in the system.
    """
    def get(self):
        """
        The `get()` method will return a list of available endpoints.
        """
        endpoints = sorted(rule.rule for rule in api.app.url_map.iter_rules())
        return {"Available endpoints": endpoints}


@api.route('/create_user/<username>')
class CreateUser(Resource):
    """
    This class supports adding user to db
    """
    def post(self, username):
        """
        this method adds user to the chatroom
        """
        return username


@api.route('/food_menu')
class FoodMenu(Resource):
    """
    This class returns the food menu to user
    """
    def get(self):
        """
        This method return the food menu
        """
        return db.get_food_menu()


@api.route('/drink_menu')
class DrinkMenu(Resource):
    """
    This class returns the food menu to user
    """
    def get(self):
        """
        This method returns the drink menu
        """
        return db.get_drink_menu()


@api.route('/room')
class Room(Resource):
    """
    This class returns the rooms to user
    """
    def get(self):
        """
        This method return the rooms
        """
        return db.get_rooms()
