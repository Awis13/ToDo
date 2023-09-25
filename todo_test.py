import unittest
import app  # Import your Flask application
import json

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()

    def test_create_task(self):
        response = self.app.post('/tasks', data=json.dumps({
            'title': 'Test Task',
            'description': 'This is a test task',
            'due_date': '2023-06-19',
            'priority': 'High'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.app.delete('/tasks/1')  # Clean up after test

    def test_get_task(self):
        self.app.post('/tasks', data=json.dumps({
            'title': 'Test Task',
            'description': 'This is a test task',
            'due_date': '2023-06-19',
            'priority': 'High'
        }), content_type='application/json')
        response = self.app.get('/tasks/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Test Task')
        self.app.delete('/tasks/1')  # Clean up after test

    def test_delete_task(self):
        self.app.post('/tasks', data=json.dumps({
            'title': 'Test Task',
            'description': 'This is a test task',
            'due_date': '2023-06-19',
            'priority': 'High'
        }), content_type='application/json')
        response = self.app.delete('/tasks/1')
        self.assertEqual(response.status_code, 204)
    def test_create_invalid_task(self):
        response = self.app.post('/tasks', data=json.dumps({
            'description': 'This is a test task',
            'due_date': '2023-06-19',
            'priority': 'High'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)  # Expect a 400 Bad Request status code

    def test_update_task(self):
        self.app.post('/tasks', data=json.dumps({
            'title': 'Test Task',
            'description': 'This is a test task',
            'due_date': '2023-06-19',
            'priority': 'High'
        }), content_type='application/json')
        response = self.app.put('/tasks/1', data=json.dumps({
            'title': 'Updated Test Task',
            'description': 'This is an updated test task',
            'due_date': '2023-06-20',
            'priority': 'Low'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)  # Expect a 200 OK status code
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Updated Test Task')  # Check that the title was updated

    def test_get_non_existent_task(self):
        response = self.app.get('/tasks/999')
        self.assertEqual(response.status_code, 404)  # Expect a 404 Not Found status code

if __name__ == '__main__':
    unittest.main()
