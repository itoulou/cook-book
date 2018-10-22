import os
import operator
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
    recipe_dict = sanitize_form_dictionary(request.form.to_dict())

    recipes.insert_one(recipe_dict)
    return redirect(url_for('all_recipes'))
    
def sanitize_form_dictionary(recipe_dict):
    try:
        recipe_dict['contain_gluten']=recipe_dict['contain_gluten']=='on'
    
    except:
        recipe_dict['contain_gluten']=False
    
    try:
        recipe_dict['contain_lactose']=recipe_dict['contain_lactose']=='on'
    
    except:
        recipe_dict['contain_lactose']=False    
    
    try:
        recipe_dict['contain_nuts']=recipe_dict['contain_nuts']=='on'
    
    except:
        recipe_dict['contain_nuts']=False    
    
    try:
        recipe_dict['batch_cook']=recipe_dict['batch_cook']=='on'
    
    except:
        recipe_dict['batch_cook']=False
        
    return recipe_dict

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
    recipe_dict = sanitize_form_dictionary(request.form.to_dict())
    
    recipes.update( {"_id": ObjectId(recipe_id)},
    
    {
        "username": recipe_dict['username'],
        "name_of_dish": recipe_dict['name_of_dish'],
        "serves": recipe_dict['serves'],
        "cuisine": recipe_dict['cuisine'],
        "ingredients": recipe_dict['ingredients'],
        "method": recipe_dict['method'],
        "contain_nuts": recipe_dict['contain_nuts'],
        "contain_gluten": recipe_dict['contain_gluten'],
        "contain_lactose": recipe_dict['contain_lactose'],
        "batch_cook": recipe_dict['batch_cook'],
        "image_url": recipe_dict['image_url']
        
        
    })
    
    return redirect(url_for('all_recipes'))
    
@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('all_recipes'))

@app.route('/gluten_free')
def sort_gluten_free():
  
    gluten_free_recipes = mongo.db.recipes.find(
                                        {'contain_gluten': {"$exists": False}})
                                        
    return render_template('glutenfree.html', gf=gluten_free_recipes)
    
@app.route('/nut_free')
def sort_nut_free():
  
    nut_free_recipes = mongo.db.recipes.find(
                                        {'contain_nuts': {"$exists": False}})
                                        
    return render_template('nutfree.html', nf=nut_free_recipes)    
    
@app.route('/lactose_free')
def sort_lactose_free():
  
    lactose_free_recipes = mongo.db.recipes.find(
                                        {'contain_lactose': {"$exists": False}})
                                        
    return render_template('lactosefree.html', lf=lactose_free_recipes)

@app.route('/batch_cook')
def sort_batch_cook():
  
    batch_cooks = mongo.db.recipes.find(
                                        {'batch_cook': {"$exists": True}})
                                        
    return render_template('batchcook.html', batch_cooks=batch_cooks)     
    

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)