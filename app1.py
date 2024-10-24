from flask import Flask, render_template, request, redirect, url_for
import matplotlib.pyplot as plt
import base64
from io import BytesIO

app = Flask(__name__)

# In-memory storage for goals (in a real application, you'd use a database)
goals = []

@app.route('/')
def home():
    return render_template('goal_tracker.html', goals=goals)

@app.route('/add_goal', methods=['POST'])
def add_goal():
    goal_name = request.form.get('goal-name')
    target_value = request.form.get('target-value', type=int)
    if goal_name and target_value is not None:
        goals.append({'name': goal_name, 'target_value': target_value, 'current_value': 0})
    return redirect(url_for('home'))

@app.route('/update_progress', methods=['POST'])
def update_progress():
    goal_id = request.form.get('goal-id', type=int)
    current_value = request.form.get('current-value', type=int)
    if goal_id is not None and 0 <= goal_id < len(goals):
        goals[goal_id]['current_value'] += current_value  # Update progress for the specified goal
    return redirect(url_for('home'))

@app.route('/visualize/<int:goal_id>')
def visualize(goal_id):
    if 0 <= goal_id < len(goals):
        goal = goals[goal_id]
        target_value = goal['target_value']
        current_value = goal['current_value']

        # Calculate progress
        days_completed = current_value
        days_left = max(0, target_value - current_value)  # Days left to achieve the goal

        # Create a pie chart with specified colors
        labels = ['Days Completed', 'Days Left']
        values = [days_completed, days_left]
        colors = ['#d91b30', '#f5b5b5']  # Pink for completed, light pink for left

        # Set the figure size to a smaller size (e.g., 4 inches by 4 inches)
        plt.figure(figsize=(4, 4))
        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
        plt.title(f'Progress for Goal: {goal["name"]}')
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Save the plot to a BytesIO object
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')  # Tight layout to minimize whitespace
        plt.close()  # Close the plot to avoid display issues
        buffer.seek(0)
        image = base64.b64encode(buffer.read()).decode('utf-8')

        return render_template('visualization.html', chart=image, goal_name=goal['name'])
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
