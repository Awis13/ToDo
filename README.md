## AI Todo List

This project is a simple Todo List application that uses OpenAI's GPT-3 to generate sarcastic comments about the tasks you add or remove. The application is built with Flask for the backend and plain JavaScript for the frontend.

### Features

Add tasks to your todo list
Delete tasks from the list
On every task addition or deletion, the application generates a sarcastic comment about your tasks
The comments are displayed in a stack from the latest to the oldest, with a maximum of 5 comments displayed at a time
The application checks the task list on every browser refresh and generates a comment about it
Setup

Clone the repository to your local machine.
Install the required Python packages using pip: pip install -r requirements.txt
Set your OpenAI API key as an environment variable: export OPENAI_API_KEY=your-api-key
Run the Flask application: python app.py
Open your web browser and navigate to http://localhost:5000 to see the application in action.
Docker

### The application can also be run using Docker. Here's how to build and run the Docker image:

Build the Docker image: docker build -t ai-todo-list .
Run the Docker container: 
```bash
docker run --rm -e OPENAI_API_KEY -p 8080:5000 ai-todo-list python -m app
```
## Testing

The application includes a basic test suite. You can run the tests with the following command: python -m unittest

### Future Improvements

Improve the UI with a modern frontend framework like React or Vue.js
Persist the tasks and comments in a database
Add user authentication to allow multiple users to have their own todo lists# ToDo
