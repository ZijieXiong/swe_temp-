# Pancake Flippers - Brunch/Casual Dining 
Restaurant Requirements
## Requirements
Information Page on what the restaurant/business is about  
<ul>
<li>Basic Menu containing:</li>  
         <ul>Food Items</ul>    
         <ul>Drinks</ul>   
<li>User should be able to see a list of the food offered in a menu</li>  
<li>users can login to the website</li>
<li>There should be two types of users: customers and managers</li>
<li>Customers have:</li>
<li>Ability to order online</li>  
<li>Ability to choose toppings and additions</li>  
<li>Ability to create a reservation</li>  
<li></li>
<li>Mangers have:</li>
<li>Ability to check all orders</li>
<li>Ability to check all reservations</li>
</ul>

## Design
<ul>
<li>Use REACT to build website for frontend</li>  
<li>Use Node/Flask for website backend (Need to ask professor)</li>  
<li>Incorporate APIs:</li>  
	 <ul>Reservation services utilizing Calenders, etc.</ul>  
	 <ul>Location services from Google</ul>  
	 <ul>Credit/Debit Card payment</ul>  
	 <ul>Paypal service</ul>   
<li>User can make a reservation by using the '\make_reservation' endpoint. User needs to type a name and choose a time slot</li>  
<li>User can view list of food items from the '\food_menu' endpoint</li>  
</ul>

## Command
<ul>
<li>make prod - build production</li>  
<li>make dev_env - create env for new developer</li>  
<li>make tests - run provided tests locally</li>  
</ul>

## TODO Immediate
<ul>
<li>Homepage</li>  
</ul>
##----------  
To build production, type `make prod`.  

To create the env for a new developer, run `make dev_env`.  
