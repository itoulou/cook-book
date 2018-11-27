import os
import operator
import json
import pymongo
from functools import wraps
from flask import Flask, render_template, redirect, request, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'online_cookbook'
app.config["MONGO_URI"] = 'mongodb://itoulou:Woro4260@ds113923.mlab.com:13923/online_cookbook'

mongo = PyMongo(app)

def session_user():
    if 'username' in session:
        return session['username']

def compare_user(recipe_id):
    session_username = session_user()
    recipe_selected = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    
    if session_username == recipe_selected['username']:
        username = session_username
    else:
        username = recipe_selected['username']
    
    return username

@app.route('/', methods=["POST", "GET"])
def login():
    users = mongo.db.users
    user = users.find_one({'username': request.form.get('username')})
    login_username = request.form.get('username')
    login_password = request.form.get('password')
    incorrect_login = 'Username or Password is incorrect'
    if user:
        if login_password == user['password']:
            session['username'] = request.form['username'] 
            return redirect(url_for('index'))
        return render_template('login.html', incorrect_login=incorrect_login) 
    
    return render_template('login.html') 

@app.route('/register', methods=["GET", "POST"])
def register():
    incorrect_login = 'Username already in use'
    if request.method == 'POST':
        users = mongo.db.users
        user = users.find_one({'username': request.form['username']})
        if user is None:
            users.insert({'username': request.form['username'],
                          'password': request.form['password']})
            session['username'] = request.form['username']              
            return redirect(url_for('index'))
            
        return render_template('register.html', incorrect_login=incorrect_login)
            
    return render_template('register.html')

@app.route('/home')
def index():
    username = session_user()
    return render_template('index.html', username=username)

@app.route('/add_recipe')
def to_add_recipe_page():
    serves = ["1", "2", "3", "4", "5", "6+"]
    cuisine = [
               "African", "American", "British", "Carribean", "Chinese",
               "East European", "French", "Greek", "Indian", "Irish",
               "Italian", "Japanese", "Korean", "Mexican",
               "Middle Eastern and Persian", "Nordic", "Spanish", "Thai",
               "Other"
                ]
    cooking_time = ["0-15 min", "15-30 min", "30-45 min", "45-60 min", "1 hr+"]            
    recipes = mongo.db.recipes.find()
    username = session_user()
    return render_template('addrecipe.html', serves=serves, cuisine=cuisine,
                            cooking_times=cooking_time, recipes=recipes,
                            username=username)
    
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes = mongo.db.recipes
    recipe_dict = sanitize_form_dictionary(request.form.to_dict())
    recipe_dict['number_of_likes'] = 0
    recipes.insert_one(recipe_dict)
    return redirect(url_for('all_recipes'))
    
def sanitize_form_dictionary(recipe_dict):
    try:
        if recipe_dict['contain_gluten']=='on' or recipe_dict['contain_gluten']=='true':
            recipe_dict['contain_gluten']=True
    except:
        recipe_dict['contain_gluten']=None

    try:
        if recipe_dict['contain_lactose']=='on' or recipe_dict['contain_lactose']=='true':
           recipe_dict['contain_lactose']=True
    except:
       recipe_dict['contain_lactose']=None
        
    try:
        if recipe_dict['contain_nuts']=='on' or recipe_dict['contain_nuts']=='true':
           recipe_dict['contain_nuts']=True
    except:
        recipe_dict['contain_nuts']=None    

    try:
        if recipe_dict['batch_cook']=='on' or recipe_dict['batch_cook']=='true':
           recipe_dict['batch_cook']=True
    except:
        recipe_dict['batch_cook']=None
        
    return recipe_dict

@app.route('/all_recipes', methods=["GET"])
def all_recipes():
    recipes = mongo.db.recipes
    total_recipe_count = mongo.db.recipes.count()
    if 'offset' in request.args:
        offset = int(request.args['offset'])
    else:
        offset = 0
    
    if 'limit' in request.args:
        limit = int(request.args['limit'])
    else:
        limit = 12
        
    starting_id = recipes.find().sort('_id', pymongo.ASCENDING)
    try:
        last_id = starting_id[offset]['_id']
        all_recipes = recipes.find({'_id': {'$gte': last_id}}).sort('_id', pymongo.ASCENDING).limit(limit)
        set_of_recipes = recipes.find({'_id': {'$gte': last_id}}).sort('_id', pymongo.ASCENDING).limit(limit)
        num_recipes = offset
        for number in set_of_recipes:
            num_recipes += 1
        next_url =  '/all_recipes?limit=' + str(limit) + '&offset=' + str(offset + limit)
        previous_url = '/all_recipes?limit=' + str(limit) + '&offset=' + str(offset - limit)
        
    except:
        page_count=0
        recipe_count = 0
        return render_template('glutenfree.html', offset=offset, limit=limit,
                                                  recipe_count=recipe_count,
                                                  page_count=page_count)
                                                  
    return render_template('allrecipes.html', recipes=all_recipes,
                                              recipe_count=total_recipe_count,
                                              next_url=next_url,
                                              previous_url=previous_url,
                                              offset=offset,
                                              limit=limit,
                                              page_count=num_recipes)
                                              
    
@app.route('/view_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    session_username = session_user()
    recipe_selected = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    name_of_dish_caps = recipe_selected['name_of_dish'].title()
    username = compare_user(recipe_id)
    return render_template('viewrecipe.html', recipe_selected=recipe_selected,
                                              name_of_dish = name_of_dish_caps,
                                              username=username,
                                              session_username=session_username)
    

@app.route('/edit_recipe/<recipe_id>')
def to_edit_recipe(recipe_id):
    serves = ["1", "2", "3", "4", "5", "6+"]
    cuisine = [
               "African", "American", "British", "Carribean", "Chinese",
               "East European", "French", "Greek", "Indian", "Irish",
               "Italian", "Japanese", "Korean", "Mexican",
               "Middle Eastern and Persian", "Nordic", "Spanish", "Thai",
               "Other"
               ]
    cooking_time = ["0-15 min", "15-30 min", "30-45 min", "45-60 min", "1 hr+"]
    recipe_selected = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    username = compare_user(recipe_id)
    return render_template('editrecipe.html', recipe=recipe_selected,
                            serves=serves, cuisine=cuisine,
                            cooking_times=cooking_time, username=username)

@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    recipes = mongo.db.recipes
    
    recipes.update( {"_id": ObjectId(recipe_id)}, sanitize_form_dictionary({
        "username": request.form.get('username'),
        "name_of_dish": request.form.get('name_of_dish'),
        "serves": request.form.get('serves'),
        "cuisine": request.form.get('cuisine'),
        "cooking_time": request.form.get('cooking_time'),
        "ingredients": request.form.get('ingredients'),
        "method": request.form.get('method'),
        "contain_gluten": request.form.get('contain_gluten'),
        "contain_lactose": request.form.get('contain_lactose'),
        "contain_nuts": request.form.get('contain_nuts'),
        "batch_cook": request.form.get('batch_cook'),
        "image_url": request.form.get('image_url')
    }))
    
    recipe_selected = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    username = recipe_selected['username']
    name_of_dish_caps = recipe_selected['name_of_dish'].title()
    session_username = session_user()
    return render_template('viewrecipe.html', recipe_selected=recipe_selected,
                                              username=username,
                                              name_of_dish=name_of_dish_caps,
                                              session_username=session_username)
    
@app.route('/num_thumb_up/<recipe_id>', methods=["POST"])
def num_thumb_up(recipe_id):
    recipes = mongo.db.recipes
    recipes.update({"_id": ObjectId(recipe_id)}, { "$inc": { "number_of_likes": 1}})
    recipe_selected = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    name_of_dish_caps = recipe_selected['name_of_dish'].title()
    username = recipe_selected['username']
    session_username = session_user()
    return render_template('viewrecipe.html', recipe_selected=recipe_selected,
                                              username=username,
                                              name_of_dish=name_of_dish_caps,
                                              session_username=session_username)

@app.route('/num_thumb_down/<recipe_id>', methods=["POST"])
def num_thumb_down(recipe_id):
    recipes = mongo.db.recipes
    recipes.update({"_id": ObjectId(recipe_id)}, { "$inc": { "number_of_likes": -1}})
    recipe_selected = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    name_of_dish_caps = recipe_selected['name_of_dish'].title()
    username = recipe_selected['username']
    session_username = session_user()
    return render_template('viewrecipe.html', recipe_selected=recipe_selected,
                                              username=username,
                                              name_of_dish=name_of_dish_caps,
                                              session_username=session_username)                                              

@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    recipes = mongo.db.recipes.find()
    return redirect(url_for('all_recipes'))

@app.route('/most_popular')
def sort_most_popular():
    recipes = mongo.db.recipes
    recipe_count = mongo.db.recipes.count()
    if 'offset' in request.args:
        offset = int(request.args['offset'])
    else:
        offset = 0
    
    if 'limit' in request.args:
        limit = int(request.args['limit'])
    else:
        limit = 12
    starting_id = recipes.find().sort('_id', pymongo.ASCENDING)
    last_id = starting_id[offset]['_id']
    all_recipes = recipes.find({'_id': {'$gte': last_id}}).sort('_id', pymongo.ASCENDING).limit(limit)
    most_popular = all_recipes.sort('number_of_likes', pymongo.DESCENDING)
    set_of_recipes = recipes.find({'_id': {'$gte': last_id}}).sort('_id', pymongo.ASCENDING).limit(limit)
    num_recipes = offset
    for number in set_of_recipes:
        num_recipes += 1
    next_url =  '/most_popular?limit=' + str(limit) + '&offset=' + str(offset + limit)
    previous_url = '/most_popular?limit=' + str(limit) + '&offset=' + str(offset - limit)
    return render_template('mostpopular.html', recipes=all_recipes,
                                               recipe_count=recipe_count,
                                               next_url=next_url,
                                               previous_url=previous_url,
                                               offset=offset,
                                               limit=limit,
                                               most_popular=most_popular,
                                               page_count=num_recipes)
    


@app.route('/gluten_free')
def sort_gluten_free():
    recipes = mongo.db.recipes
    recipe_count = mongo.db.recipes.count({'contain_gluten': None})
    if 'offset' in request.args:
        offset = int(request.args['offset'])
    else:
        offset = 0
    
    if 'limit' in request.args:
        limit = int(request.args['limit'])
    else:
        limit = 12
        
    starting_id = recipes.find({'contain_gluten': None}).sort('_id', pymongo.ASCENDING)
    
    try:    
        last_id = starting_id[offset]['_id']
        all_recipes = recipes.find({'_id': {'$gte': last_id}, 'contain_gluten': None}).limit(limit)
        set_of_recipes = recipes.find({'_id': {'$gte': last_id}, 'contain_gluten': None}).limit(limit)
        num_recipes = offset
        for number in set_of_recipes:
            num_recipes += 1
        next_url =  '/gluten_free?limit=' + str(limit) + '&offset=' + str(offset + limit)
        previous_url = '/gluten_free?limit=' + str(limit) + '&offset=' + str(offset - limit)
    
    except:
        page_count=0
        recipe_count = 0
        return render_template('glutenfree.html', offset=offset, limit=limit,
                                                  recipe_count=recipe_count,
                                                  page_count=page_count)
                                                  
    return render_template('glutenfree.html', recipes=all_recipes,
                                              recipe_count=recipe_count,
                                              next_url=next_url,
                                              previous_url=previous_url,
                                              offset=offset,
                                              limit=limit,
                                              page_count=num_recipes)
    
    
@app.route('/nut_free')
def sort_nut_free():
    recipes = mongo.db.recipes
    recipe_count = mongo.db.recipes.count({'contain_nuts': None})
    if 'offset' in request.args:
        offset = int(request.args['offset'])
    else:
        offset = 0
    
    if 'limit' in request.args:
        limit = int(request.args['limit'])
    else:
        limit = 12
    starting_id = recipes.find({'contain_nuts': None}).sort('_id', pymongo.ASCENDING)
    
    try:    
        last_id = starting_id[offset]['_id']
        all_recipes = recipes.find({'_id': {'$gte': last_id}, 'contain_nuts': None}).limit(limit)
        set_of_recipes = recipes.find({'_id': {'$gte': last_id}, 'contain_nuts': None}).limit(limit)
        num_recipes = offset
        for number in set_of_recipes:
            num_recipes += 1
        next_url =  '/nut_free?limit=' + str(limit) + '&offset=' + str(offset + limit)
        previous_url = '/nut_free?limit=' + str(limit) + '&offset=' + str(offset - limit)
    
    except:
        page_count=0
        recipe_count = 0
        return render_template('nutfree.html', offset=offset, limit=limit,
                                                  recipe_count=recipe_count,
                                                  page_count=page_count)
                                                  
    return render_template('nutfree.html', recipes=all_recipes,
                                              recipe_count=recipe_count,
                                              next_url=next_url,
                                              previous_url=previous_url,
                                              offset=offset,
                                              limit=limit,
                                              page_count=num_recipes)
    
     
    
@app.route('/lactose_free')
def sort_lactose_free():
    recipes = mongo.db.recipes
    recipe_count = mongo.db.recipes.count({'contain_lactose': None})
    if 'offset' in request.args:
        offset = int(request.args['offset'])
    else:
        offset = 0
    
    if 'limit' in request.args:
        limit = int(request.args['limit'])
    else:
        limit = 12
    starting_id = recipes.find({'contain_lactose': None}).sort('_id', pymongo.ASCENDING)
    try:    
        last_id = starting_id[offset]['_id']
        all_recipes = recipes.find({'_id': {'$gte': last_id}, 'contain_lactose': None}).limit(limit)
        set_of_recipes = recipes.find({'_id': {'$gte': last_id}, 'contain_lactose': None}).limit(limit)
        num_recipes = offset
        for number in set_of_recipes:
            num_recipes += 1
        next_url =  '/lactose_free?limit=' + str(limit) + '&offset=' + str(offset + limit)
        previous_url = '/lactose_free?limit=' + str(limit) + '&offset=' + str(offset - limit)
    
    except:
        page_count = 0
        recipe_count = 0
        return render_template('lactosefree.html', offset=offset, limit=limit,
                                                  recipe_count=recipe_count,
                                                  page_count=page_count)
                                                  
    return render_template('lactosefree.html', recipes=all_recipes,
                                              recipe_count=recipe_count,
                                              next_url=next_url,
                                              previous_url=previous_url,
                                              offset=offset,
                                              limit=limit,
                                              page_count=num_recipes)

@app.route('/batch_cook')
def sort_batch_cook():
    recipes = mongo.db.recipes
    recipe_count = mongo.db.recipes.count({'batch_cook': True})
    if 'offset' in request.args:
        offset = int(request.args['offset'])
    else:
        offset = 0
    
    if 'limit' in request.args:
        limit = int(request.args['limit'])
    else:
        limit = 12
        
    starting_id = recipes.find({'batch_cook': True}).sort('_id', pymongo.ASCENDING)
    
    try:    
        last_id = starting_id[offset]['_id']
        all_recipes = recipes.find({'_id': {'$gte': last_id}, 'batch_cook': None}).limit(limit)
        set_of_recipes = recipes.find({'_id': {'$gte': last_id}, 'batch_cook': None}).limit(limit)
        num_recipes = offset
        for number in set_of_recipes:
            num_recipes += 1
        next_url =  '/batch_cook?limit=' + str(limit) + '&offset=' + str(offset + limit)
        previous_url = '/batch_cook?limit=' + str(limit) + '&offset=' + str(offset - limit)
    
    except:
        page_count = 0
        recipe_count = 0
        return render_template('batchcook.html', offset=offset, limit=limit,
                                                  recipe_count=recipe_count,
                                                  page_count=page_count)
   
    return render_template('batchcook.html', recipes=all_recipes,
                                              recipe_count=recipe_count,
                                              next_url=next_url,
                                              previous_url=previous_url,
                                              offset=offset,
                                              limit=limit,
                                              page_count=num_recipes)


if __name__ == '__main__':
    app.secret_key = 'my_secret_key'
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)