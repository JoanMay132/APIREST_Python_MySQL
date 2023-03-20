from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, ValidationError



app= Flask(__name__) # Flask instance
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:@localhost:3306/apachito' # Connection to the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False # Disable the tracking of modifications

db=SQLAlchemy (app) # Database instance
#ma=Schema(app) # Marshmallow instance

# creation ot the category table
class Category(db.Model): 
    cat_id=db.Column(db.Integer, primary_key=True) # Primary key
    cat_name=db.Column(db.String(100))
    cat_description=db.Column(db.String(100))

    def __init__(self, cat_name, cat_description):
        self.cat= cat_name
        self.cat_description= cat_description

with app.app_context():
    db.create_all() # Create the table

# Schema for the category table
class categorySchema(Schema):
    class Meta:
        fields=('cat_id','cat_name','cat_description')

# Just one request

category_schema=categorySchema() # Instance of the category schema

# Many requests
categories_schema=categorySchema(many=True) # Instance of the category schema

# Get all categories

@app.route('/categorie', methods=['GET'])
def get_categories():
    all_categories=Category.query.all() # Get all categories
    result=categories_schema.dump(all_categories) # Dump the categories
    return jsonify(result)

# GET PER ID ################################################

@app.route('/categorie/<id>', methods=['GET'])
def get_category(id):
    a_category=Category.query.get(id) # Get the category by id
    return category_schema.dump(a_category) # Dump the category

# POST #####################################################
@app.route('/categorie', methods=['POST'])
def add_category():
    data=request.get_json(force=True)
    cat_name=request.json['cat_name']
    cat_description=request.json['cat_description']

    new_record=Category(cat_name, cat_description) # Create a new category

    db.session.add(new_record) # Add the new category to the database
    db.session.commit() # Commit the changes
    return category_schema.dump(new_record) # Dump the new category

# PUT ######################################################

@app.route('/categorie/<id>', methods=['PUT']) # Route to update a category
def update_category(id):
    updatecategory=Category.query.get(id) # Get the category by id

    cat_name=request.json['cat_name']
    cat_description=request.json['cat_description']

    updatecategory.cat_name=cat_name # Update the category name
    updatecategory.cat_description=cat_description # Update the category description

    db.session.commit() # Commit the changes
    return category_schema.dump(updatecategory) # Dump the category

# DELETE ###################################################
@app.route('/categorie/<id>', methods=['DELETE']) # Route to delete a category
def delete_category(id):
    deletecategory=Category.query.get(id) # Get the category by id
    db.session.delete(deletecategory) # Delete the category
    db.session.commit() # Commit the changes
    return category_schema.dump(deletecategory) # Dump the category
#Mensaje de Bienvenida

@app.route('/',methods=['GET']) # Route to the main page
def index():
    return jsonify({'message':'Hello World'})

if __name__=='__main__':
    app.run(debug=True) # Initialize the app