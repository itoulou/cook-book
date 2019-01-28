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
* __All recipes__
* __Most popular__
* __Gluten Free__
* __Nut Free__
* __Lactose Free__
* __Suitable for batch cooking__



* __User Issues and Features__ - If a user has posted any issues or feature requests
they will appear on their page with the option to choose which will be visible
by clicking on the buttons 'My issues' and 'My features'.
    * Screens greater than 992px width have pagination where they can switch pages
    by clicking 'next' or 'previous'
    
    * Screens less than 992px have no pagination.

### Issue Tracker
* __All Issues__ - User can see all the issues by clicking 'Issues' button in navbar
    * All issues are paginated every 9 issues displaying the title, votes, number
    of comments, icon showing if Issue has been sorted or not and 'View issue' button. 
    * User can view the particular issue by clicking either on the title or the
    'View issue' button.
    * If there are no comments on a particular issue, user can click 'Be the first to comment'
    where they will directed precisely to the 'Add comment' button on the viewissue.html page.
    * User can create a ticket by clicking 'Create a Ticket' where they will need to fill out a form
    with a title of the issue and content of the issue and a tag. 
    * User can search for a specific issue by name using the search form on the all issues page.
    If the search returns nothing a message will pop up saying 'Unfortunately your search didn't find anything'.

* __View issue__ 
    * Any user can vote for the issue signalling that they have this issue
    too by clikcing the chevron where the vote number will increase by 1 if toggled once
    and decreased by 1 if toggled again.
    * The author of the user can display whether or not the issue has been fixed by clicking
    * the 'Done' button which will produce a red tick signalling that the issue has been fixed,
    letting other users know that they have the same issue, they can find the solution here.
    * Only the author of the issue can edit an issue. If they wish to do so then
    they can click 'Edit issue' where they will be redirected to a form similar to that of 'Create a Ticket'.
    * Only the author can delete the issue if they wish by clikcing 'Delete issue'.
    * Any user can comment if they wish by clicking 'Add comment' by a which a modal will
    appear where they would fill out a form with their comment content. This comment
    will be displayed on the viewed issue page itself. 
        * If there are more than 3 comments on that page then a button named 'View comments'
        will appear whereby if clicked a modal will appear representing all the comments shown.
        * All comments are in blockquote form where the user profile image is displayed next to their comment.
    * Screens with width greater than 992px will have a 'Back' button displayed which will redirect them
    back to the all issues page.

### Feature Requests
* __Requests behave in the exact same way as issue tracker except for a change depending
on whether the user is subscribed or has already paid.__
    * In order for a user to upvote a feature they must be subscribed. If user
    is not subscribed and they try and vote, then user will be redirected to a checkout
    form where they will fill out an address and card form with the price of £5.99.
    * If user pays for this then they can vote for that particular feature but not any others.
    * If user is subscribed they are able to vote for any feature.

### Future features to implement
* __Include graphs and figures__
    * Representing the issues or features with the highest votes.
    * Most common issues/feature ideas judging by similarity of titles.
    * Perhaps in the future, in order to help my business model, represnt the
    speed it takes me to fix issues and develop features.
* Have the ability to add friends and share your own issues and feature ideas with them.

# Technologies used
* [__HTML__](https://devdocs.io/html/) 
    * This project uses HTML to provide the content.
* [__CSS__](https://devdocs.io/css/) 
    * This project uses CSS to provide the styles.
* [__Bootstrap__](https://getbootstrap.com/docs/3.3/getting-started/)
    * This project uses Bootstrap framework to simplify grid layout and provide a better UX. 
* [__JQuery__](https://api.jquery.com/)
    * This project uses Jquery to simplify DOM manipulation and provide better UX.
* [__Python__](https://docs.python.org/release/3.4.3/)
    * This project uses Python to handle POSTs and manipulate data presented from the user. 
* [__Django__](https://docs.djangoproject.com/en/1.11/)
    * This project uses Django framework to provide a useful and comprehensible toolkit to a  build an effective web application. 
* [__SQLite__](https://www.sqlite.org/docs.html)
    * This project uses SQLite as database to use locally.
* [__PostgreSQL__](https://www.postgresql.org/docs/)
    * This project uses PostgreSQL as a database to use globally.
* [__Amazon Web Services (AWS)__](https://docs.aws.amazon.com/index.html#lang/en_us)
    * This project uses AWS (S3) as a means of storing media and static files. 
* [__Stripe__](https://stripe.com/gb)
    * This project uses Stripe as a payment service for users and to ensure that all security checks are dealt with. 

# Testing
### Login Form
1. Go to 'Login' page.
2. Try to submit the empty form and verify that an error message about the required fields appears.
3. Try to submit the form with an invalid email address and verify that a relevant error message appears.
4. Try to submit the form with all inputs valid and verify you are redirected to the homepage where a success message appears.

### Register Form
1. Go to 'Register' page.
2. Try to submit the empty form and verify that an error message about the required fields appears.
3. Try to submit the form with an email address already in use and verify that a relevant error message appears.
4. Try to submit the form with username already in use and verify that a relevant error message appears.
5. Try to submit the form with two different password and verify that a relevant error message appears.
6. Try to submit the form with all inputs valid and verify you are redirected to the homepage where a success message appears.

### Subscription Address Form
1. Click on the 'Subscribe' button.
2. Try to submit the empty form and verify that an error message about the required fields appears.
3. Try to submit the form without any address details except 'County' and verify that a relevant error message appears.
4. Try to submit the form with all inputs valid and verify you are redirected to the homepage where a success message appears and subscribe button changes to 'Unsubscribe'.

### Profile Picture Form
1. Click on either the image or 'Add a profile picture'.
2. Try to submit the empty form and verify that an error message about the required fields appears.
3. Try to submit the form with a valid image then image appears and options to change or remove image appear.
4. Same testing applies when 'Change profile picture is clicked'.

### My Issues and My Features
1. Click either 'My Issues' or 'My Features' and user's items appear.
2. If user has no issues posted or feature requests posted a message appears with option to create one.

### Create/Edit Issue and Create/Edit Feature
1. Click 'Create Ticket'/'Create Request'/'Edit Issue'/'Edit Feature'.
2. Try to submit the empty form and verify that an error message about the required fields appears.
3. Try to submit the form with all inputs valid and verify you are redirected to item just created or edited with details 
just submitted from previous form.

### Search
1. Type in the input
2. If words match then it will return all issues and feature requests relative to the 
information given from the user.
3. Try to submit an empty form and returns everything as normal.
4. If search doesn't match with any items in the database then error message appears.


### Comments
1. Click 'Add comment'.
2. Try to submit the empty form and verify that an error message about the required fields appears.
3. Try to submit the form with all inputs valid and verify you are redirected to view issue/feature page where your comment
appears with the user profile image.

### Voting for Feature
1. Click chevron icon to upvote feature.
2. If user subscribed and chevron clicked number of votes increases by 1.
3. If user is not subscribed they are redirected to Checkout page.

### Checkout page
2. Try to submit the empty form and verify that an error message about the required fields appears.
3. Try to submit the form without any address details except 'County' and verify that a relevant error message appears.
4. Try to submit the form with all inputs valid and verify you are redirected to the 'view issue' page where a success message appears 
5. Try to vote for same feature and vote number should increase by 1.
6. Try to vote for different feature and verify you are redirected to 'checkout' page.

[![Build Status](https://travis-ci.org/itoulou/unicorn-attractor.svg?branch=master)](https://travis-ci.org/itoulou/unicorn-attractor)

# Deployment
I have deployed this project to the hosting platform [__Heroku__](https://devcenter.heroku.com/categories/reference)
with a separate [__GitHub__](https://github.com/) branch.
### Config Vars
* AWS_ACCESS_KEY_ID
* AWS_SECRET_ACCESS_KEY
* DATABASE_URL
* DISABLE_COLLECTSTATIC
* SECRET_KEY
* STRIPE_PUBLISHABLE
* STRIPE_SECRET

# Credits
### Acknowledgments
* A big thank you to Victor Miclovich my mentor who's been extremely helpful with
the completion of this project.
* Another big thank you to all the Tutors at Code Institute for coping with my multitude of questions on a daily basis.