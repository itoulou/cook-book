# Online Cookbook - <a href="http://online-cookbook-tou.herokuapp.com/" target="_blank">The Pantry</a>

The brief for this assignment was to produce an online cookbook where users can
store and easily access cooking recipes. 

No need to buy any more magazines or cook books! The Pantry is a web application
where users can share and look for recipes of their favourite foods and drinks.
Whether it be a classic dish with a twist or something never seen before, it's 
very easy for users to post a recipe. All you need to do is register with 
a username and password and you can share as many recipes with the world as you please.

# UX

This web application is for anyone who loves to cook, eager to start cooking or
looking for new ideas or fancies trying to broaden their culinary horizons.
This app is also useful for those who work long hours and want to save those precious
minutes by cooking large one pot meals suitable for refridgerating or freezing for when you come home and don't
have any energy left to cook and wash up but still want something guilt free and
delicious.

As people suffer from all varieties of allergens such as nuts, lactose and gluten,
I wanted to allow users to filter recipes based on their allergies to provide them
a wide choice of recipes to follow.

Some users may not have a lot of time to cook their own food and rely on quick
fast food but would prefer to eat healthier home cooked food. I wanted to
provide a section dedicated to these users where you can search for recipes that 
are suitable for cooking several portions and able to reheat later, essentially
cooking half a week's worth of food in one batch covering 6-8 meals.

### All Recipes
__md/lg__

![all recipes image](/wireframes/images/all-recipes-md-lg.png "all recipes md lg")

__xs/sm__

![all recipes image](/wireframes/images/all-recipes-xs-sm.png "all recipes xs sm")

### View Recipe
__md/lg__

![view recipe image](/wireframes/images/view-recipe-md-lg.png "view recipe md lg")

__xs/sm__

![view recipe image](/wireframes/images/view-recipe-xs-sm.png "view recipe xs sm")

# Features
### Login
* __Login__
    * Users can login to the web application if they are already registered by
    filling out login form.

### Register
* __Register__
    * Users can register to the web application by filling out the register form.

### Base
* __Navbar__
    *  At screen width greater than 992px, Navbar will be visible in the top-right corner.
    *  At screen width below 992px, Navbar will be present by the click of a Hamburger
    button in the top left corner.

### Homepage
* __Fine recipe__ 
    * User can click the 'Find recipe' button to redirect them to all the recipes
    on the app.
* __Add recipe__
    * User can click the 'Add recipe' button to redirect them to the 'add recipe'
    page.

### Add recipe
* User can add a recipe to the database to share publically by filling out the 
form on the 'add recipe' page.

### Filter
* User can click the 'Filter' button and display the following options:
    * __All recipes__
        * User can select to view all recipes in the order that they are created.
    * __Most popular__
        * User can filter recipes by the number of likes 
    * __Gluten Free__
        * User can filter recipes to display gluten free only  
    * __Nut Free__
        * User can filter recipes to display nut free only  
    * __Lactose Free__
        * User can filter recipes to display lactose free only  
    * __Suitable for batch cooking__
        * User can filter recipes to display the ones suitable to cooking in several batches
        at once.

### Up voting
* __Voting for recipe__ 
    * User can vote for any recipe they like by clicking the thumbs up button. 
    If they wish to remove their vote they can do so by just toggling the like button
    again.

### Update recipe and Delete recipe
* If the user is the creator of the recipe then they are able to update their recipe
by filling out the 'update recipe' form or delete the recipe by clicking the 'Delete'
button.

# Technologies used
* [__HTML__](https://devdocs.io/html/) 
    * This project uses HTML to provide the content.
* [__CSS__](https://devdocs.io/css/) 
    * This project uses CSS to provide the styles.
* [__Materialize__](https://materializecss.com/getting-started.html)
    * This project uses Materialize framework to simplify grid layout and provide a better UX. 
* [__JQuery__](https://api.jquery.com/)
    * This project uses Jquery to simplify DOM manipulation and provide better UX.
* [__Python__](https://docs.python.org/release/3.4.3/)
    * This project uses Python to handle POSTs and manipulate data presented from the user.
* [__Flask__](http://flask.pocoo.org/docs/1.0/)
    * This project uses Flask to create URLs easily and use a tool to simplify the creation of this web application . 
* [__mLab__](https://docs.mlab.com/)
    * This project uses mLab as the NoSQL database.

# Testing
### Login Form
1. Go to 'Login' page.
2. Try to submit the empty form and verify that an error message about the required fields appears.
3. Try to submit the form with an invalid username or password and verify that a relevant error message appears.
4. Try to submit the form with all inputs valid and verify you are redirected to the index page.

### Register Form
1. Go to 'Register' page.
2. Try to submit the empty form and verify that an error message about the required fields appears.
3. Try to submit the form with an email address already in use and verify that a relevant error message appears.
4. Try to submit the form with username already in use and verify that a relevant error message appears.
6. Try to submit the form with all inputs valid and verify you are redirected to the homepage where a success message appears.

### Add Recipe and Edit Recipe Form
1. Click on the 'Add recipe' button.
2. Try to submit the empty form and verify that an error message about the required fields appears.
3. Try to submit the form with all inputs valid and verify you are redirected to the 'all recipes' page.

### Like/Up vote
1. Click the thumb icon to turn it blue.
2. Verify that username of the user who liked the recipes is added to an array under 'liked_by' key in database.
3. Verify that 'number_of_likes' is incremented by 1.
4. Click the thumb icon again so it turns white.
5. Verify that username of the user who liked the recipes is removed from array.
6. Verify that 'number_of_likes' is decremented by 1.

### Pagination
1. Verify that both chevron buttons are disabled when recipe count is less than 12.
2. When recipe count is greater than 12, verify that right chevron is no longer disabled.
2. If right chevron clicked then verify next set of 12 recipes is displayed and left chevron no longer disabled.
3. If left chevron clicked then verify that previous set of 12 is displayed.

# Deployment
I have deployed this project to the hosting platform [__Heroku__](https://devcenter.heroku.com/categories/reference)
with a separate [__GitHub__](https://github.com/) branch.
### Config Vars
* IP
* PORT

# Credits
### Acknowledgments
* A big thank you to Victor Miclovich my mentor who's been extremely helpful with
the completion of this project.
* Another big thank you to all the Tutors at Code Institute for coping with my multitude of questions on a daily basis.