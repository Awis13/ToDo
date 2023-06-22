from flask import Flask, request, render_template, jsonify
import openai
import os

app = Flask(__name__, static_folder='static')

# Set up the OpenAI API
openai.api_key = os.environ['OPENAI_API_KEY']
conversation_history = [
    {"role": "system", "content": "You are a grumpy old AI, very fun and sarcastic. Your job is to comment on users task list."},
]

# Define the Task class
class Task:
    def __init__(self, title, description, due_date, priority):
        self.id = len(tasks) + 1  # Generate unique ID
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority

# Initialize an empty tasks list
tasks = []

# Placeholder tasks
tasks.extend([
    Task("Buy groceries", "Need to restock the fridge", "2023-06-20", "High"),
    Task("Clean house", "Its a mess", "2023-06-25", "Medium"),
    Task("Clean bathroom", "PLEASE!", "2023-07-01", "Low"),
])  



# Function for natural language processing
def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    )

    message = response.choices[0].message['content']
    return message

@app.route('/')
def index():
    return render_template('index.html')

# Route for natural language processing
@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.form['prompt']
    message = generate_response(prompt)
    return message

@app.route('/tasks', methods=['POST'])
def create_task():
    task_data = request.get_json()
    required_fields = ['title', 'description', 'due_date', 'priority']
    if not all(field in task_data for field in required_fields):
        return 'Bad Request: Missing required field', 400
    task = Task(task_data['title'], task_data['description'], task_data['due_date'], task_data['priority'])
    tasks.append(task)
    return task.__dict__, 201

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify([task.__dict__ for task in tasks]), 200

@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = next((task for task in tasks if task.id == id), None)
    if task is None:
        return 'Task not found', 404
    return jsonify(task.__dict__), 200

@app.route('/generate_comment', methods=['POST'])
def generate_comment():
    task_data = request.get_json()
    before = task_data['before']
    after = task_data['after']
    
    # Add the new user message to the conversation history
    conversation_history.append({"role": "user", "content": f"The task list has changed from {before} to {after}."})
    
    # Generate response using conversation history
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation_history
    )
    
    # Get assistant's reply from the response
    message = response.choices[0].message['content']
    
    # Add the assistant's reply to the conversation history
    conversation_history.append({"role": "assistant", "content": message})
    
    return jsonify({'comment': message})
	
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    if id < 0 or id >= len(tasks):
        return 'Task not found', 404
    task_data = request.get_json()
    task = tasks[id]
    task.title = task_data['title']
    task.description = task_data['description']
    task.due_date = task_data['due_date']
    task.priority = task_data['priority']
    return jsonify(task.__dict__), 200

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = next((task for task in tasks if task.id == id), None)
    if task is None:
        return 'Task not found', 404
    tasks.remove(task)
    return '', 204


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
