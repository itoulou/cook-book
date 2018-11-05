import os
import operator
import json
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
        if recipe_dict['contain_gluten']=='on':
            recipe_dict['contain_gluten']=True
    except:
        recipe_dict['contain_gluten']=False

    try:
        if recipe_dict['contain_lactose']=='on':
           recipe_dict['contain_lactose']=True
    except:
        recipe_dict['contain_lactose']=False
        
    try:
        if recipe_dict['contain_nuts']=='on':
           recipe_dict['contain_nuts']=True
    except:
        recipe_dict['contain_nuts']=False    

    try:
        if recipe_dict['batch_cook']=='on':
           recipe_dict['batch_cook']=True
    except:
        recipe_dict['batch_cook']=False
        
    return recipe_dict



@app.route('/all_recipes')
def all_recipes():
    user = mongo.db.users.find()
    all_recipes = mongo.db.recipes.find()
    return render_template('findrecipe.html', recipes=all_recipes, user=user)

@app.route('/view_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    session_username = session_user()
    recipe_selected = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    
    username = compare_user(recipe_id)

    return render_template('viewrecipe.html', recipe_selected=recipe_selected,
                                              username=username)
    


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
    return render_template('viewrecipe.html', recipe_selected=recipe_selected)
    
@app.route('/num_thumb_up/<recipe_id>', methods=["POST"])
def num_thumb_up(recipe_id):
    recipes = mongo.db.recipes
    recipes.update({"_id": ObjectId(recipe_id)}, { "$inc": { "number_of_likes": 1}})
    recipe_selected = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    return render_template('viewrecipe.html', recipe_selected=recipe_selected)
    
@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('all_recipes'))

@app.route('/gluten_free')
def sort_gluten_free():
    gluten_free_recipes = mongo.db.recipes.find({'contain_gluten': False})
    return render_template('glutenfree.html', gf=gluten_free_recipes)
    
@app.route('/nut_free')
def sort_nut_free():
    nut_free_recipes = mongo.db.recipes.find({'contain_nuts': False})
    return render_template('nutfree.html', nf=nut_free_recipes)    
    
@app.route('/lactose_free')
def sort_lactose_free():
    lactose_free_recipes = mongo.db.recipes.find({'contain_lactose': False})
    return render_template('lactosefree.html', lf=lactose_free_recipes)

@app.route('/batch_cook')
def sort_batch_cook():
    batch_cooks = mongo.db.recipes.find({'batch_cook': True})
    return render_template('batchcook.html', batch_cooks=batch_cooks)     
    

if __name__ == '__main__':
    app.secret_key = 'my_secret_key'
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)