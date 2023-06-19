from flask import Flask, request
import openai
import os

app = Flask(__name__)

# Set up the OpenAI API
openai.api_key = os.environ['OPENAI_API_KEY']

# Define the Task class
class Task:
    def __init__(self, title, description, due_date, priority):
        self.id = len(tasks) + 1  # Generate unique ID
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority

tasks = []  # This will hold our tasks for now

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

# Route for natural language processing
@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.form['prompt']
    message = generate_response(prompt)
    return message


@app.route('/tasks', methods=['POST'])
def create_task():
    task_data = request.get_json()
    task = Task(task_data['title'], task_data['description'], task_data['due_date'], task_data['priority'])
    tasks.append(task)
    return task.__dict__, 201

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return [task.__dict__ for task in tasks], 200

@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = next((task for task in tasks if task.id == id), None)
    if task is None:
        return 'Task not found', 404
    return task.__dict__, 200

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
    return task.__dict__, 200

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    if id < 0 or id >= len(tasks):
        return 'Task not found', 404
    del tasks[id]
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
