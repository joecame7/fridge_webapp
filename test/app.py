from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from flask_cors import CORS
from datetime import datetime, timedelta
import os
import json
import random
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fridgegenie2025'
CORS(app)

@app.template_filter('strptime')
def strptime_filter(date_string, format):
    return datetime.strptime(date_string, format)

# Register the filter
app.jinja_env.filters['strptime'] = strptime_filter

# Mock database for demonstration
class Database:
    def __init__(self):
        self.items = [
            {
                "id": 1,
                "name": "Milk",
                "barcode": "5000128677424",
                "quantity": 1,
                "expiry_date": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),
                "category": "Dairy",
                "image_url": "https://cdn.pixabay.com/photo/2017/07/05/15/41/milk-2474993_640.jpg"
            },
            {
                "id": 2,
                "name": "Cheddar Cheese",
                "barcode": "5000328748591",
                "quantity": 1,
                "expiry_date": (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"),
                "category": "Dairy",
                "image_url": "https://cdn.pixabay.com/photo/2016/03/05/19/24/cheese-1238395_640.jpg"
            },
            {
                "id": 3,
                "name": "Eggs",
                "barcode": "0012345678905",
                "quantity": 6,
                "expiry_date": (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d"),
                "category": "Dairy",
                "image_url": "https://cdn.pixabay.com/photo/2015/09/17/17/25/egg-944495_640.jpg"
            },
            {
                "id": 4,
                "name": "Apples",
                "barcode": "0023456789012",
                "quantity": 4,
                "expiry_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
                "category": "Fruits",
                "image_url": "https://cdn.pixabay.com/photo/2017/09/26/13/21/apples-2788599_640.jpg"
            },
            {
                "id": 5,
                "name": "Chicken Breast",
                "barcode": "0034567890123",
                "quantity": 1,
                "expiry_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
                "category": "Meat",
                "image_url": "https://cdn.pixabay.com/photo/2016/05/30/15/25/chicken-1424886_640.jpg"
            }
        ]
        
        self.recipes = [
            {
                "id": 1,
                "name": "Apple Cinnamon Pancakes",
                "ingredients": ["Apples", "Eggs", "Milk", "Flour", "Cinnamon"],
                "image_url": "https://spoonacular.com/recipeImages/635350-556x370.jpg",
                "instructions": "Mix flour, eggs, and milk. Fold in diced apples and cinnamon. Cook on a hot griddle until golden brown."
            },
            {
                "id": 2,
                "name": "Chicken and Cheese Quesadillas",
                "ingredients": ["Chicken Breast", "Cheddar Cheese", "Tortillas", "Onions"],
                "image_url": "https://spoonacular.com/recipeImages/641908-556x370.jpg",
                "instructions": "Shred cooked chicken, mix with cheese. Place on tortilla, fold, and cook until cheese melts."
            },
            {
                "id": 3,
                "name": "Cheese Omelette",
                "ingredients": ["Eggs", "Cheddar Cheese", "Milk", "Butter"],
                "image_url": "https://spoonacular.com/recipeImages/642085-556x370.jpg",
                "instructions": "Beat eggs with milk, pour into hot buttered pan, add cheese, fold when partially set."
            }
        ]
        
        self.settings = {
            "notifications": True,
            "expiry_alert_days": 3,
            "door_open_alert": True,
            "temperature_threshold": 4.0,
            "light_threshold": 500,
            "motion_threshold": 0.8
        }
        
        self.sensor_data = {
            "temperature": 3.2,
            "door_status": "closed",
            "last_opened": (datetime.now() - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S"),
            "light_level": 0,
            "motion_detected": False
        }
        
    def get_all_items(self):
        return self.items
        
    def get_item(self, item_id):
        for item in self.items:
            if item["id"] == item_id:
                return item
        return None
        
    def add_item(self, item):
        item_id = max([i["id"] for i in self.items], default=0) + 1
        item["id"] = item_id
        self.items.append(item)
        return item
        
    def update_item(self, item_id, updated_data):
        for i, item in enumerate(self.items):
            if item["id"] == item_id:
                self.items[i].update(updated_data)
                return self.items[i]
        return None
        
    def delete_item(self, item_id):
        for i, item in enumerate(self.items):
            if item["id"] == item_id:
                return self.items.pop(i)
        return None
        
    def get_recommended_recipes(self):
        # Simple algorithm to recommend recipes based on available ingredients
        available_ingredients = [item["name"] for item in self.items]
        recommended = []
        
        for recipe in self.recipes:
            matching_ingredients = 0
            for ingredient in recipe["ingredients"]:
                if ingredient in available_ingredients:
                    matching_ingredients += 1
            
            # If more than half the ingredients are available, recommend it
            if matching_ingredients >= len(recipe["ingredients"]) / 2:
                recipe_copy = recipe.copy()
                recipe_copy["matching_ingredients"] = matching_ingredients
                recipe_copy["total_ingredients"] = len(recipe["ingredients"])
                recommended.append(recipe_copy)
                
        # Sort by highest percentage of matching ingredients
        recommended.sort(key=lambda x: x["matching_ingredients"] / x["total_ingredients"], reverse=True)
        return recommended
        
    def get_settings(self):
        return self.settings
        
    def update_settings(self, updated_settings):
        self.settings.update(updated_settings)
        return self.settings
        
    def get_sensor_data(self):
        # Simulate some randomness in sensor data for the demo
        self.sensor_data["temperature"] = round(random.uniform(3.0, 8.0), 1)
        
        # Randomly open the door sometimes
        if random.random() < 0.1:
            self.sensor_data["door_status"] = "open"
            self.sensor_data["light_level"] = random.randint(500, 1000)
            self.sensor_data["motion_detected"] = True
            self.sensor_data["last_opened"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.sensor_data["door_status"] = "closed"
            self.sensor_data["light_level"] = random.randint(0, 50)
            self.sensor_data["motion_detected"] = False
            
        return self.sensor_data
        
    def get_expiring_items(self, days=3):
        today = datetime.now().date()
        expiring = []
        
        for item in self.items:
            expiry_date = datetime.strptime(item["expiry_date"], "%Y-%m-%d").date()
            days_until_expiry = (expiry_date - today).days
            
            if 0 <= days_until_expiry <= days:
                expiring.append({
                    "item": item,
                    "days_left": days_until_expiry
                })
                
        return expiring

# Initialize db
db = Database()

# Routes
@app.route('/')
def home():
    sensor_data = db.get_sensor_data()
    expiring_items = db.get_expiring_items(db.get_settings()["expiry_alert_days"])
    return render_template('home.html', 
                          sensor_data=sensor_data, 
                          expiring_items=expiring_items)

@app.route('/items')
def items():
    items = db.get_all_items()
    current_time = datetime.now().strftime('%Y-%m-%d')
    return render_template('items.html', items=items, current_time=current_time)

@app.route('/item/<int:item_id>')
def item_details(item_id):
    item = db.get_item(item_id)
    if not item:
        flash('Item not found', 'error')
        return redirect(url_for('items'))
    return render_template('item_details.html', item=item, now=datetime.now, timedelta=timedelta)

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        new_item = {
            "name": request.form.get('name'),
            "barcode": request.form.get('barcode'),
            "quantity": int(request.form.get('quantity')),
            "expiry_date": request.form.get('expiry_date'),
            "category": request.form.get('category'),
            "image_url": request.form.get('image_url', '')
        }
        db.add_item(new_item)
        flash('Item added successfully', 'success')
        return redirect(url_for('items'))
    return render_template('add_item.html')

@app.route('/edit_item/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    item = db.get_item(item_id)
    if not item:
        flash('Item not found', 'error')
        return redirect(url_for('items'))
        
    if request.method == 'POST':
        updated_data = {
            "name": request.form.get('name'),
            "barcode": request.form.get('barcode'),
            "quantity": int(request.form.get('quantity')),
            "expiry_date": request.form.get('expiry_date'),
            "category": request.form.get('category'),
            "image_url": request.form.get('image_url', item['image_url'])
        }
        db.update_item(item_id, updated_data)
        flash('Item updated successfully', 'success')
        return redirect(url_for('item_details', item_id=item_id))
        
    return render_template('edit_item.html', item=item, now=datetime.now, timedelta=timedelta)

@app.route('/delete_item/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    item = db.delete_item(item_id)
    if item:
        flash('Item deleted successfully', 'success')
    else:
        flash('Item not found', 'error')
    return redirect(url_for('items'))

@app.route('/scan_barcode')
def scan_barcode():
    # In a real application, this would interface with camera
    # For demo purposes, we'll simulate scanning
    return render_template('scan_barcode.html')

@app.route('/lookup_barcode', methods=['POST'])
def lookup_barcode():
    barcode = request.form.get('barcode')
    
    # Call the OpenFoodFacts API to get product information
    api_url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    
    try:
        response = requests.get(api_url)
        data = response.json()
        
        if data.get('status') == 1:  # Product found
            product_data = data.get('product', {})
            
            product = {
                "name": product_data.get('product_name', 'Unknown Product'),
                "category": product_data.get('categories_tags', ['unknown'])[0].replace('en:', '').capitalize(),
                "image_url": product_data.get('image_url', '')
            }
        else:
            # Product not found in database
            product = {
                "name": "Unknown Product",
                "category": "Other",
                "image_url": ""
            }
    except Exception as e:
        # Handle any errors (connection issues, etc.)
        print(f"Error fetching product data: {e}")
        product = {
            "name": "Unknown Product",
            "category": "Other",
            "image_url": ""
        }
    
    # Add the barcode and default values
    product["barcode"] = barcode
    product["quantity"] = 1
    product["expiry_date"] = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    
    return render_template('lookup_barcode.html', item=product)

@app.route('/recipes')
def recipes():
    recommended_recipes = db.get_recommended_recipes()
    return render_template('recipes.html', recipes=recommended_recipes)

@app.route('/recipe/<int:recipe_id>')
def recipe_details(recipe_id):
    for recipe in db.recipes:
        if recipe["id"] == recipe_id:
            return render_template('recipe_details.html', recipe=recipe)
    
    flash('Recipe not found', 'error')
    return redirect(url_for('recipes'))

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        updated_settings = {
            "notifications": 'notifications' in request.form,
            "expiry_alert_days": int(request.form.get('expiry_alert_days')),
            "door_open_alert": 'door_open_alert' in request.form,
            "temperature_threshold": float(request.form.get('temperature_threshold')),
            "light_threshold": int(request.form.get('light_threshold')),
            "motion_threshold": float(request.form.get('motion_threshold'))
        }
        db.update_settings(updated_settings)
        flash('Settings updated successfully', 'success')
        return redirect(url_for('settings'))
        
    return render_template('settings.html', settings=db.get_settings())

@app.route('/api/sensor_data')
def api_sensor_data():
    return jsonify(db.get_sensor_data())

@app.route('/api/items')
def api_items():
    return jsonify(db.get_all_items())

@app.route('/api/expiring_items')
def api_expiring_items():
    days = request.args.get('days', db.get_settings()["expiry_alert_days"], type=int)
    return jsonify(db.get_expiring_items(days))

@app.route('/api/recipes')
def api_recipes():
    return jsonify(db.get_recommended_recipes())

# Create templates directory if it doesn't exist
if not os.path.exists('templates'):
    os.makedirs('templates')

# Create static directory if it doesn't exist
if not os.path.exists('static'):
    os.makedirs('static')
    
if not os.path.exists('static/css'):
    os.makedirs('static/css')
    
if not os.path.exists('static/js'):
    os.makedirs('static/js')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)