import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'online_cookbook'
app.config["MONGO_URI"] = 'mongodb://itoulou:Woro4260@ds113923.mlab.com:13923/online_cookbook'

mongo = PyMongo(app)

@app.route('/')
def return_home():
    return render_template('index.html')
    
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
    recipes = mongo.db.recipes.find()            
    return render_template('addrecipe.html', serves=serves, cuisine=cuisine,
                            recipes=recipes)
    
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes = mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    return redirect(url_for('all_recipes'))

@app.route('/all_recipes')
def all_recipes():
    all_recipes = mongo.db.recipes.find()
    return render_template('findrecipe.html', recipes=all_recipes)

@app.route('/view_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    recipe_selected = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    return render_template('viewrecipe.html', recipe_selected=recipe_selected)

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
    recipe_selected =  mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template('editrecipe.html', recipe=recipe_selected, serves=serves, cuisine=cuisine)

@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    recipes = mongo.db.recipes
    recipes.update( {"_id": ObjectId(recipe_id)},
    
    {
        "username": request.form.get('username'),
        "name_of_dish": request.form.get('name_of_dish'),
        "serves": request.form.get('serves'),
        "cuisine": request.form.get('cuisine'),
        "ingredients": request.form.get('ingredients'),
        "method": request.form.get('method'),
        "contain_nuts": request.form.get('contain_nuts'),
        "contain_gluten": request.form.get('contain_gluten'),
        "contain_lactose": request.form.get('contain_lactose'),
        "batch_cook": request.form.get('batch_cook'),
        "image_url": request.form.get('image_url')
        
        
    })
    return redirect(url_for('all_recipes'))

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)