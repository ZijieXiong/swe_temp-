"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

from http import HTTPStatus
from flask import Flask
from flask_restx import Resource, Api, reqparse
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


@api.route('/user/register/<userName>&<password>&<int:type>')
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


@api.route('/user/delete/<userName>')
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


@api.route('/food_menu/new/<foodName>&<foodType>&<int:price>&<foodDes>')
class NewFoodItem(Resource):
    """
    This class creates a new food item for the menu
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'NOT FOUND')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'A duplicate key')
    def post(self, foodName, foodType, price, foodDes):
        """
        This method adds a new food item the food_menu db
        """
        ret = db.add_food_item(foodName, foodType, price, foodDes)
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


food_parser = reqparse.RequestParser()
food_parser.add_argument('new_foodName', type=str, help='new_foodName')
food_parser.add_argument('new_foodType', type=str, help='new_foodType')
food_parser.add_argument('new_price', type=int, help='new_price')
food_parser.add_argument('new_description', type=str, help='new_description')


@api.route('/food_menu/update/<foodName>')
class UpdateFoodItem(Resource):
    """
    This class updates an existing food item from the food menu
    """
    @api.doc(parser=food_parser)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'NOT FOUND')
    def post(self, foodName):
        """
        This method will update a food item from the food_menu db
        """
        args = drink_parser.parse_args()
        new_foodName = args['new_foodName']
        new_foodType = args['new_foodType']
        new_price = args['new_price']
        new_description = args['new_description']
        ret = db.update_food_item(
            foodName, new_foodName, new_foodType, new_price, new_description)
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


@api.route('/food_menu/list/<typeName>')
class ListFoodByType(Resource):
    """
    This class returns a dictionary of all food of specific type
    """
    def post(self, typeName):
        """
        This method fetch all foods of a specific type from db
        """
        return db.get_food_by_type(typeName)


@api.route('/food_menu/type')
class ListFoodType(Resource):
    """
    This class returns the food types to user
    """
    def get(self):
        """
        This method returns the food types
        """
        return db.get_food_type()


@api.route('/food_menu/type/add/<typeName>')
class AddFoodType(Resource):
    """
    This class adds a new food type to the foodType db
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'A duplicate key')
    def post(self, typeName):
        """
        This method adds a food type to the db
        """
        ret = db.add_food_type(typeName)
        if ret == db.DUPLICATE:
            raise(wz.NotAcceptable("Item could not be found."))
        else:
            return "food item updated"


@api.route('/drink_menu/new/<drinkName>&<drinkType>&<int:price>&<drinkDes>')
class NewDrinkItem(Resource):
    """
    This class adds a new drink item to the drink db
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'NOT FOUND')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'A duplicate key')
    def post(self, drinkName, drinkType, price, drinkDes):
        """
        This method adds a new drink item to the drink_menu db
        """
        ret = db.add_drink_item(drinkName, drinkType, price, drinkDes)
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


drink_parser = reqparse.RequestParser()
drink_parser.add_argument('new_drinkName', type=str, help='new_drinkName')
drink_parser.add_argument('new_drinkType', type=str, help='new_drinkType')
drink_parser.add_argument('new_price', type=int, help='new_price')
drink_parser.add_argument('new_description', type=str, help='new_description')


@api.route('/drink_menu/update/<drinkName>')
class UpdateDrinkItem(Resource):
    """
    This class updates an existing drink item from the drink menu
    """
    @api.doc(parser=drink_parser)
    @api.response(HTTPStatus.OK, 'SUCCESS')
    @api.response(HTTPStatus.NOT_FOUND, 'NOT_FOUND')
    def post(self, drinkName):
        """
        This method will update a drink item from the drink_menu db
        """
        args = drink_parser.parse_args()
        new_drinkName = args['new_drinkName']
        new_drinkType = args['new_drinkType']
        new_price = args['new_price']
        new_description = args['new_description']
        ret = db.update_drink_item(drinkName, new_drinkName,
                                   new_drinkType, new_price, new_description)
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


order_parser = reqparse.RequestParser()
order_parser.add_argument('foodName', action='split')
order_parser.add_argument('drinkName', action='split')
order_parser.add_argument('foodQuanti', type=int, action='split')
order_parser.add_argument('drinkQuanti', type=int, action='split')


@api.route('/order/new/<userName>&<specialReqs>&<orderType>&<phoneNum>')
class NewOrder(Resource):
    """
    This class adds a new order to the database.
    """
    @api.doc(parser=order_parser)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'NOT FOUND')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Incorrect items input')
    def post(self, userName, specialReqs, orderType, phoneNum):
        """
        This method adds a new order to the order db.
        """
        args = order_parser.parse_args()
        foodName = args["foodName"]
        drinkName = args["drinkName"]
        foodQuanti = args['foodQuanti']
        drinkQuanti = args['drinkQuanti']
        ret = db.add_order(userName, foodName, drinkName, foodQuanti,
                           drinkQuanti, specialReqs, orderType, phoneNum)
        if ret == db.NOT_FOUND:
            raise(wz.NotAcceptable("Items not exist"))
        if ret == db.NOT_ACCEPTABLE:
            raise(wz.NotAcceptable(
                'Incorrect length between names and quantities.'))
        else:
            return "order added"


@api.route('/order/list')
class ListOrder(Resource):
    """
    This class returns a dictionary of all orders
    """
    def get(self):
        """
        This method fetch the orders from the order db.
        """
        return db.get_order_list()


@api.route('/order/user/<userName>')
class ListOrderByUser(Resource):
    """
    This class returns a dictionary of all orders by a specifc user
    """
    def post(self, userName):
        """
        This method fetch the orders by a specifc from the order db.
        """
        return db.get_order_by_user(userName)


@api.route('/drink_menu/type/<typeName>')
class ListDrinkByType(Resource):
    """
    This class returns a dictionary of all drinks of a specific type
    """
    def post(self, typeName):
        """
        This method fetch all drinks of a specific type from db
        """
        return db.get_drink_by_type(typeName)


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


@api.route('/drink_menu/type/add/<typeName>')
class AddDrinkType(Resource):
    """
    This class adds a new drink type to drinkType db
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'A duplicate key')
    def post(self, typeName):
        """
        This methods adds a drink type to the db
        """
        ret = db.add_drink_type(typeName)
        if ret == db.DUPLICATE:
            raise(wz.NotAcceptable("Item could not be found."))
        else:
            return "food item updated"


@api.route('/review_list/<review>')
class NewReview(Resource):
    """
    This class adds a new feedback string to feedback db
    """
    def post(self, review):
        """
        This method adds the feedback to the feedback db
        """
        db.add_review(review)
        return "review added"


@api.route('/review_list/review')
class ListReviews(Resource):
    """
    This class lists every review
    """
    def get(self):
        """
        This method lists every review
        """
        return db.get_review_list()
