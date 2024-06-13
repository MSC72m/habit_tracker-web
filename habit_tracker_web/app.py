from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime, timedelta
from flask import request

app = Flask(__name__)

def load_habits():
    try:
        with open('habits.json', 'r') as file:
            habits = json.load(file)
            # Ensure each habit has an ID
            for index, habit in enumerate(habits, start=1):
                habit.setdefault('id', index)
    except (FileNotFoundError, json.JSONDecodeError, Exception) as e:
        habits = [] 
        print(f"Error loading habits: {str(e)}")  
    return habits


def save_habits(habits):
    try:
        with open('habits.json', 'w') as file:
            json.dump(habits, file, indent=4)
    except Exception as e:
        print(f"Error saving habits: {str(e)}") 


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

def ensure_habits_have_ids():
    habits = load_habits()
    for index, habit in enumerate(habits, start=1):
        if 'id' not in habit:
            habit['id'] = index
    save_habits(habits)


@app.route('/')
def home():
    habits = load_habits()
    return render_template('home.html', habits=habits)


if __name__ == '__main__':
    app.run(debug=True)
