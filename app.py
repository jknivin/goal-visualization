from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage for goals (in a real application, you'd use a database)
goals = []

@app.route('/')
def home():
    return render_template('goal_tracker.html', goals=goals)

@app.route('/add_goal', methods=['POST'])
def add_goal():
    goal = request.form.get('goal')
    if goal:
        goals.append(goal)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
