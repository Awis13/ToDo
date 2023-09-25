import unittest
import json
from app import app, get_db  # Import your Flask application and database function

class TestApp(unittest.TestCase):
	def setUp(self):
		self.app = app.test_client()

	def tearDown(self):
		with app.app_context():
			db = get_db()
			db.execute('DELETE FROM tasks')
			db.commit()

	def test_create_task(self):
		response = self.app.post('/tasks', data=json.dumps({
			'title': 'Test Task',
			'description': 'This is a test task',
			'due_date': '2023-06-19',
			'priority': 'High'
		}), content_type='application/json')
		self.assertEqual(response.status_code, 201)

	def test_get_task(self):
		response = self.app.post('/tasks', data=json.dumps({
			'title': 'Test Task',
			'description': 'This is a test task',
			'due_date': '2023-06-19',
			'priority': 'High'
		}), content_type='application/json')
		task_id = json.loads(response.data)['id']
		response = self.app.get(f'/tasks/{task_id}')
		self.assertEqual(response.status_code, 200)
		data = json.loads(response.data)
		self.assertEqual(data['title'], 'Test Task')

	def test_delete_task(self):
		response = self.app.post('/tasks', data=json.dumps({
			'title': 'Test Task',
			'description': 'This is a test task',
			'due_date': '2023-06-19',
			'priority': 'High'
		}), content_type='application/json')
		task_id = json.loads(response.data)['id']
		response = self.app.delete(f'/tasks/{task_id}')
		self.assertEqual(response.status_code, 204)

	# ... (rest of your test methods)

if __name__ == '__main__':
	unittest.main()
