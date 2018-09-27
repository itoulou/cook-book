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
    return render_template('addrecipe.html')
    
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes = mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    return redirect(url_for('return_home'))

@app.route('/all_recipes')
def all_recipes():
    all_recipes = mongo.db.recipes.find()
    return render_template('findrecipe.html', recipes=all_recipes)

@app.route('/view_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    recipe_selected = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    return render_template('viewrecipe.html', recipe_selected=recipe_selected)

@app.route('/edit_recipe')
def to_edit_recipe():
    render_template('editrecipe.html')

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)