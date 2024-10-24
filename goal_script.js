document.getElementById('goal-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const goalName = document.getElementById('goal-name').value;
    const targetValue = document.getElementById('target-value').value;
    
    // Call a function to send data to the backend
    // For example, using fetch to send a POST request
    fetch('/set_goal', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ goal_name: goalName, target_value: targetValue })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        loadGoals(); // Reload goals after setting a new one
    });
});

document.getElementById('progress-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const goalId = document.getElementById('goal-id').value;
    const currentValue = document.getElementById('current-value').value;

    // Call a function to update the goal progress
    fetch('/update_progress', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ goal_id: goalId, current_value: currentValue })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        loadGoals(); // Reload goals after updating progress
    });
});

function loadGoals() {
    fetch('/get_goals')
        .then(response => response.json())
        .then(goals => {
            const goalList = document.getElementById('goal-list');
            goalList.innerHTML = ''; // Clear previous goals
            goals.forEach(goal => {
                const goalItem = document.createElement('div');
                goalItem.textContent = `Goal: ${goal.goal_name}, Target: ${goal.target_value}, Current: ${goal.current_value}`;
                goalList.appendChild(goalItem);
            });
        });
}

document.getElementById('visualize-btn').addEventListener('click', function() {
    // Function to visualize goal progress, possibly using a library like Chart.js
    // For now, you can alert the user or call an API to generate the visualization
    alert('Visualization feature coming soon!');
});

// Load goals on page load
window.onload = loadGoals;
