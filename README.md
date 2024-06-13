# Flask Habit Tracker

## Project Description
This project is a web-based habit tracker built using the Flask framework. Users can add, complete, and remove habits. The habit data is stored in a JSON file (`habits.json`), ensuring persistence across sessions.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Routes and Functionality](#routes-and-functionality)
- [Code Explanation](#code-explanation)

## Installation
1. Clone the repository.
2. Install the required packages using pip:
    ```bash
    pip install flask
    ```
3. Ensure you have a `habits.json` file in the same directory as the script. If not, the script will create an empty one for you.

## Usage
To run the project, use the following command:
```bash
python app.py
```
This will start the Flask development server. Open your web browser and navigate to http://127.0.0.1:5000 to use the habit tracker.

## Routes and Functionality
The application has the following routes and functionalities:

### Home Route (/)
### Displays the list of habits.
 Template: home.html
### Add Habit Route (/add_habit)
 Method: GET, POST
### Displays a form to add a new habit.
Template: add_habit.html
### Complete Habit Route (/complete_habit)
 Method: POST
 Marks a habit as completed, incrementing its streak count.
### Remove Habit Route (/remove_habit)
Method: POST
Removes a habit from the list based on its ID.
## Code Explanation
Importing Libraries
```python

from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime, timedelta
```
These import statements bring in the necessary libraries and modules for the Flask application, JSON handling, and date/time manipulation.

### Flask Application Setup
``` python

app = Flask(__name__)
This initializes the Flask application.

Load Habits Function
python
Copy code
def load_habits():
    try:
        with open('habits.json', 'r') as file:
            habits = json.load(file)
            for index, habit in enumerate(habits, start=1):
                habit.setdefault('id', index)
    except (FileNotFoundError, json.JSONDecodeError, Exception) as e:
        habits = []
        print(f"Error loading habits: {str(e)}")
    return habits
```
Loads the habits from the habits.json file.
Ensures each habit has an ID.
Handles file not found and JSON decode errors gracefully.
Save Habits Function
``` python

def save_habits(habits):
    try:
        with open('habits.json', 'w') as file:
            json.dump(habits, file, indent=4)
    except Exception as e:
        print(f"Error saving habits: {str(e)}")
```
Saves the habits to the habits.json file.
Handles errors that may occur during the save process.
Add Habit Form Route
``` python

@app.route('/add_habit', methods=['GET', 'POST'])
def add_habit_form():
    if request.method == 'POST':
        habits = load_habits()
        name = request.form.get('habit_name')
        habit_id = max(habit['id'] for habit in habits) + 1 if habits else 1
        habit = {'id': habit_id, 'name': name, 'streak': 0, 'modified_time': str(datetime.now().date())}
        habits.append(habit)
        save_habits(habits)
        return redirect(url_for('home'))
    return render_template('add_habit.html')
```
Displays a form to add a new habit.
On form submission, saves the new habit and redirects to the home page.
Complete Habit Route
``` python

@app.route('/complete_habit', methods=['POST'])
def complete_habit():
    habit_id = request.form.get('habit_id')
    if habit_id and habit_id.isdigit():
        habit_id = int(habit_id)
        habits = load_habits()
        found = False
        for habit in habits:
            if habit.get('id') == habit_id:
                habit['streak'] += 1
                found = True
                break
        if found:
            save_habits(habits)
            return redirect(url_for('home'))
        else:
            return "No habit found with provided ID", 404
    return "Invalid habit ID", 400
```
Marks a habit as completed by incrementing its streak.
Validates the habit ID and handles errors if the ID is not found or invalid.
Remove Habit Route
``` python

@app.route('/remove_habit', methods=['POST'])
def remove_habit():
    habit_id = request.form.get('habit_id')
    if habit_id and habit_id.isdigit():
        habit_id = int(habit_id)
        habits = load_habits()
        found = False
        for index, habit in enumerate(habits):
            if habit.get('id') == habit_id:
                del habits[index]
                found = True
                break
        if found:
            save_habits(habits)
            return redirect(url_for('home'))
        else:
            return "No habit found with provided ID", 404
    return "Invalid habit ID", 400
```
Removes a habit from the list based on its ID.
Validates the habit ID and handles errors if the ID is not found or invalid.
Ensure Habits Have IDs Function
``` python

def ensure_habits_have_ids():
    habits = load_habits()
    for index, habit in enumerate(habits, start=1):
        if 'id' not in habit:
            habit['id'] = index
    save_habits(habits)
```
Ensures all habits have unique IDs.
Home Route
``` python

@app.route('/')
def home():
    habits = load_habits()
    return render_template('home.html', habits=habits)
Displays the list of habits.
Template: home.html
```
Main Function
``` python

if __name__ == '__main__':
    app.run(debug=True)
```
Runs the Flask application in debug mode.
