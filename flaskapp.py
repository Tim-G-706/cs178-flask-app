# author: T. Urness and M. Moore
# description: Flask example using redirect, url_for, and flash
# credit: the template html files were constructed with the help of ChatGPT

import re
from collections import defaultdict
from boto3.dynamodb.conditions import Attr
from flask import Flask
from flask import render_template
from flask import Flask, render_template, request, redirect, url_for, flash
from dbCode import *

app = Flask(__name__)
app.secret_key = 'your_secret_key' # this is an artifact for using flash displays; 
                                   # it is required, but you can leave this alone


@app.route('/')
def home():
    restaurants = execute_query("SELECT * FROM restaurants ");
    return render_template('home.html', results = restaurants)

@app.route('/add-visit', methods=['GET', 'POST'])
def add_visit():
    if request.method == 'POST':
        restaurant_name = request.form.get('restaurant_name')
        total_spent = request.form.get('total_spent')
        rating = request.form.get('rating')

        #The following function was generated with help from ChatGPT
        #Since apparently the NoSQL data output from the html is stored in strings
        #and getting indexes and values from within a string is very confusing
        people = defaultdict(lambda: {"items": []})

        for key, value in request.form.items():

            # Match: people[0][name]
            name_match = re.match(r'people\[(\d+)\]\[name\]', key)
            if name_match:
                p_idx = int(name_match.group(1))
                people[p_idx]["name"] = value

            # Match: people[0][items][0][item_name]
            item_match = re.match(r'people\[(\d+)\]\[items\]\[(\d+)\]\[(.+)\]', key)
            if item_match:
                p_idx = int(item_match.group(1))
                i_idx = int(item_match.group(2))
                field = item_match.group(3)

                # Ensure item exists
                while len(people[p_idx]["items"]) <= i_idx:
                    people[p_idx]["items"].append({})

                people[p_idx]["items"][i_idx][field] = value

        # Convert dict → ordered list
        people_list = [people[i] for i in sorted(people.keys())]

        # Final structured object
        visit = {
            "Restaurant": restaurant_name,
            "total_spent": total_spent,
            "rating": rating,
            "people": people_list
        }

        #Save to DynamoDB
        table.put_item(Item=visit)
        execute_query("UPDATE restaurants SET has_visited = 1 WHERE name = %s", (restaurant_name,));
        
        flash('Visit added successfully! Huzzah!', 'success')  # 'success' is a category; makes a green banner at the top
        # Redirect to home page or another page upon successful submission
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('add_visit.html')

@app.route('/delete-user',methods=['GET', 'POST'])
def delete_user():
    if request.method == 'POST':
        # Extract form data
        name = request.form['name']
        
        # Process the data (e.g., add it to a database)
        # For now, let's just print it to the console
        print("Name to delete:", name)
        
        flash('User deleted successfully! Hoorah!', 'warning') 
        # Redirect to home page or another page upon successful submission
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('delete_user.html')


@app.route('/display-visit', methods=['GET', 'POST'])
def display_visit():
    selected_name = request.args.get('Restaurant', '')

    response = table.scan()
    all_items = response.get('Items', [])
    restaurant_names = list(set(item['Restaurant'] for item in all_items))
    visits = []
    if selected_name:
        for item in all_items:
            if item['Restaurant'] == selected_name:
                visits.append(item)
    return render_template('display_visit.html', Restaurant = selected_name, visits = visits, restaurant_names = restaurant_names)


# these two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
