"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

from http import HTTPStatus
from flask import Flask
from flask_restx import Resource, Api
from flask_cors import CORS
import db.db as db
import werkzeug.exceptions as wz
app = Flask(__name__)
api = Api(app)
HELLO = 'hello'
cors = CORS(app)


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


@api.route('/reserve/list')
class ListReservation(Resource):
    """
    This class returns the list of reservations to user
    """
    def get(self):
        """
        This method return the reservations list
        """
        return db.get_reserve()


@api.route('/reserve/create/<userName>&<time>&<int:numOfPeople>')
class CreateReserve(Resource):
    """
    This class create a new record of reservation
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'NOT FOUND')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'A duplicate key')
    def post(self, userName, time, numOfPeople):
        """
        This method adds a reservation record to reservation db
        """
        ret = db.add_reserve(userName, time, numOfPeople)
        if ret == db.DUPLICATE:
            raise(wz.NotAcceptable("Reservation already exists."))
        else:
            return "new order added."


@api.route('/reserve/delete/<userName>&<time>')
class DeleteReserve(Resource):
    """
    This class deletes an existing record of a reservation
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'User not found')
    def post(self, userName, time):
        """
        this method deletes an existing reservation record from the
        reservation db
        """
        ret = db.delete_reserve(userName, time)
        if ret == db.NOT_FOUND:
            raise(wz.NotAcceptable("Reservation could not be found."))
        else:
            return "Reservation deleted"


@api.route('/reserve/update/<userName>&<time>&<newTime>&<int:newNumOfPeople>')
class UpdateReserve(Resource):
    """
    This class updates an existing record of a reservation
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Reservation not found')
    def post(self, userName, time, newTime, newNumOfPeople):
        """
        this method updates an existing reservation record
        from the reservation db
        """
        ret = db.update_reserve(userName, time, newTime, newNumOfPeople)
        if ret == db.NOT_FOUND:
            raise(wz.NotAcceptable("Reservation could not be found."))
        else:
            return "Reservation updated"


@api.route('/register/<userName>&<password>&<int:type>')
class RegisterUser(Resource):
    """
    This class create a new record of a user
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'A duplicate key')
    def post(self, userName, password, type):
        """
        this method adds a new user to user db
        """
        ret = db.add_user(userName, password, type)
        if ret == db.DUPLICATE:
            raise(wz.NotAcceptable("User already exists."))
        else:
            return "new user added"


@api.route('/register/<userName>')
class DeleteUser(Resource):
    """
    This class deletes an existing record of a specific user
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'User not found')
    def post(self, userName):
        """
        this method deletes a user from the user db
        """
        ret = db.delete_user(userName)
        if ret != db.NOT_FOUND:
            raise(wz.NotAcceptable("User could not be found."))
        else:
            return "User deleted"


@api.route('/login/<userName>&<password>')
class LogIn(Resource):
    """
    This class check if the user name and
    password matched the record in database.
    """
    def post(self, userName, password):
        """
        this method checks if user name and
        password exists in database and
        return the type of the user.
        return 0 if not matched.
        """
        if(userName != ""):
            if(db.user_exists(userName)):
                user = db.get_user(userName)
                if(user["password"] == password):
                    return(user["type"])
        return 0


@api.route('/food_menu/new/<foodName>')
class NewFoodItem(Resource):
    """
    This class creates a new food item for the menu
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'NOT FOUND')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'A duplicate key')
    def post(self, foodName):
        """
        This method adds a new food item the food_menu db
        """
        ret = db.add_food_item(foodName)
        if ret == db.DUPLICATE:
            raise(wz.NotAcceptable("Food Item already exists."))
        else:
            return "food item added."


@api.route('/food_menu/delete/<foodName>')
class DeleteFoodItem(Resource):
    """
    This class deletes an existing food item from the menu
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'NOT FOUND')
    def post(self, foodName):
        """
        This method will delete a food item from the food_menu db
        """
        ret = db.delete_food_item(foodName)
        if ret == db.NOT_FOUND:
            raise(wz.NotAcceptable("Item could not be found."))
        else:
            return "food item deleted."


@api.route('/food_menu/update/<foodName>&<new_foodName>')
class UpdateFoodItem(Resource):
    """
    This class updates an existing food item from the food menu
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'NOT FOUND')
    def post(self, foodName, new_foodName):
        """
        This method will update a food item from the food_menu db
        """
        ret = db.update_food_item(foodName, new_foodName)
        if ret == db.NOT_FOUND:
            raise(wz.NotAcceptable("Item could not be found."))
        else:
            return "food item updated"


@api.route('/food_menu/list')
class ListFoodMenu(Resource):
    """
    This class returns the food menu
    """
    def get(self):
        """
        This method returns the food menu
        """
        return db.get_food_menu()


@api.route('/drink_menu/new/<drinkName>')
class NewDrinkItem(Resource):
    """
    This class adds a new drink item to the drink db
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'NOT FOUND')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'A duplicate key')
    def post(self, drinkName):
        """
        This method adds a new drink item to the drink_menu db
        """
        ret = db.add_drink_item(drinkName)
        if ret == db.DUPLICATE:
            raise(wz.NotAcceptable("Drink Item already exists."))
        else:
            return "drink item added"


@api.route('/drink_menu/delete/<drinkName>')
class DeleteDrinkItem(Resource):
    """
    This call deletes an existing drink item from drink menu
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'NOT_FOUND')
    def post(self, drinkName):
        """
        This methods attempts to delete a drink item from drink menu
        """
        ret = db.delete_drink_item(drinkName)
        if ret == db.NOT_FOUND:
            raise(wz.NotAcceptable("Item could not be found."))
        else:
            return "drink item deleted."


@api.route('/drink_menu/update/<drinkName>&<new_drinkName>')
class UpdateDrinkItem(Resource):
    """
    This class updates an existing drink item from the drink menu
    """
    @api.response(HTTPStatus.OK, 'SUCCESS')
    @api.response(HTTPStatus.NOT_FOUND, 'NOT_FOUND')
    def post(self, drinkName, new_drinkName):
        """
        This method will update a drink item from the drink_menu db
        """
        ret = db.update_drink_item(drinkName, new_drinkName)
        if ret == db.NOT_FOUND:
            raise(wz.notAcceptable("Item could not be found"))
        else:
            return "drink item updated"


@api.route('/drink_menu/list')
class ListDrinkMenu(Resource):
    """
    This class returns the drink menu to user
    """
    def get(self):
        """
        This method returns the drink menu
        """
        return db.get_drink_menu()


@api.route('/drink_menu/type')
class ListDrinkType(Resource):
    """
    This class returns the drink types to user
    """
    def get(self):
        """
        This method returns the drink types
        """
        return db.get_drink_type()
