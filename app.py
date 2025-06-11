from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Required to use sessions

# Sample food database by meal and goal
meal_options = {
    'gain': {
        'Breakfast': ['Oats with milk and banana', 'Peanut butter toast', 'Paneer paratha'],
        'Lunch': ['Rice with dal and chicken', 'Chapati with rajma', 'Curd rice with boiled eggs'],
        'Dinner': ['Grilled paneer with vegetables', 'Chapati with chole', 'Quinoa with chicken curry']
    },
    'lose': {
        'Breakfast': ['Boiled eggs and fruit', 'Oats with skimmed milk', 'Smoothie with spinach and banana'],
        'Lunch': ['Grilled chicken salad', 'Chapati with sabzi', 'Lentil soup with salad'],
        'Dinner': ['Steamed vegetables with tofu', 'Soup and salad', 'Chapati with dal']
    },
    'maintain': {
        'Breakfast': ['Upma', 'Idli with sambar', 'Vegetable poha'],
        'Lunch': ['Rice with dal', 'Chapati with vegetable curry', 'Curd rice'],
        'Dinner': ['Chapati with mixed sabzi', 'Khichdi', 'Vegetable stew']
    }
}

def generate_weekly_meal_plan(goal):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    plan = {}
    for day in days:
        plan[day] = {
            'Breakfast': random.choice(meal_options[goal]['Breakfast']),
            'Lunch': random.choice(meal_options[goal]['Lunch']),
            'Dinner': random.choice(meal_options[goal]['Dinner'])
        }
    return plan

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        age = int(request.form['age'])
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        activity = request.form['activity']
        condition = request.form['condition']
        goal = request.form['goal']

        bmi = round(weight / ((height / 100) ** 2), 1)
        category = 'underweight' if bmi < 18.5 else 'normal' if bmi < 25 else 'overweight'
        water_goal = round(weight * 0.033, 2)

        # Basic food suggestions
        base_foods = {
            'gain': ['🥪 Peanut butter sandwiches', '🥛 Whole milk', '🍌 Bananas', '🥜 Dry fruits'],
            'lose': ['🥗 Salads', '🍎 Apples', '🥒 Cucumber', '🍲 Soups'],
            'maintain': ['🍚 Rice', '🍛 Dal', '🥦 Mixed vegetables']
        }

        weekly_meal_plan = generate_weekly_meal_plan(goal)

        result = {
            'bmi': bmi,
            'category': category,
            'water_goal': water_goal,
            'activity': activity,
            'condition': condition,
            'goal': goal,
            'foods': base_foods[goal],
            'weekly_meal_plan': weekly_meal_plan
        }

        session['result'] = result  # store result in session
        return redirect(url_for('summary'))  # redirect to summary page

    return render_template('index.html')

@app.route('/summary')
def summary():
    result = session.get('result', None)
    if not result:
        return redirect(url_for('index'))
    return render_template('summary.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
