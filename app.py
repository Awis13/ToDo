import openai
import os
from flask import Flask, render_template, request, jsonify, g
import sqlite3

app = Flask(__name__, static_folder='static')

# Set up the OpenAI API
openai.api_key = os.environ['OPENAI_API_KEY']
conversation_history = [
    {"role": "system", "content": "You are a grumpy old AI, very fun and sarcastic. Your job is to comment on users' task list."},
]

DATABASE = 'tasks.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                due_date TEXT,
                priority TEXT
            )
        ''')
        db.commit()


class Task:
    def __init__(self, title, description, due_date, priority):
        self.id = None  # Will be set when saving to the database
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority

    def save(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO tasks (title, description, due_date, priority)
            VALUES (?, ?, ?, ?)
        ''', (self.title, self.description, self.due_date, self.priority))
        db.commit()
        self.id = cursor.lastrowid

    @staticmethod
    def get_all():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT id, title, description, due_date, priority FROM tasks')
        rows = cursor.fetchall()
        tasks = []
        for row in rows:
            id, title, description, due_date, priority = row
            task = Task(title, description, due_date, priority)
            task.id = id
            tasks.append(task)
        return tasks

    @staticmethod
    def get_by_id(id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT id, title, description, due_date, priority FROM tasks WHERE id = ?', (id,))
        row = cursor.fetchone()
        if row is not None:
            id, title, description, due_date, priority = row
            task = Task(title, description, due_date, priority)
            task.id = id
            return task
        return None

    def update(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            UPDATE tasks
            SET title = ?, description = ?, due_date = ?, priority = ?
            WHERE id = ?
        ''', (self.title, self.description, self.due_date, self.priority, self.id))
        db.commit()

    def delete(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (self.id,))
        db.commit()


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
    task.save()
    return task.__dict__, 201


@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.get_all()
    return jsonify([task.__dict__ for task in tasks]), 200


@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.get_by_id(id)
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
    task_data = request.get_json()
    task = Task.get_by_id(id)
    if task is None:
        return 'Task not found', 404
    task.title = task_data['title']
    task.description = task_data['description']
    task.due_date = task_data['due_date']
    task.priority = task_data['priority']
    task.update()
    return jsonify(task.__dict__), 200


@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.get_by_id(id)
    if task is None:
        return 'Task not found', 404
    task.delete()
    return '', 204


if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
