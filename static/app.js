document.addEventListener('DOMContentLoaded', () => {
	const taskInput = document.getElementById('task-input');
	const addTaskBtn = document.getElementById('add-task-btn');
	const taskList = document.getElementById('task-list');
	const commentBox = document.getElementById('comment-box');

	// Function to create a new task item
	function createTaskItem(taskText, taskId) {
		const taskItem = document.createElement('li');
		taskItem.textContent = taskText;

		// Create the delete button
		const deleteBtn = document.createElement('button');
		deleteBtn.textContent = 'X';
		deleteBtn.classList.add('delete-btn');
		deleteBtn.addEventListener('click', () => {
			// Delete the task on the client side
			taskItem.remove();

			// Delete the task on the server
			fetch(`/tasks/${taskId}`, {
				method: 'DELETE',
			})
				.then(response => {
					if (!response.ok) {
						throw new Error('Error: ' + response.statusText);
					}
					updateTasks();
				})
				.catch(error => console.error('Error:', error));
		});

		taskItem.appendChild(deleteBtn);
		taskList.appendChild(taskItem);
	}

	// Fetch all tasks when the page loads
	fetch('/tasks')
		.then(response => response.json())
		.then(tasks => {
			tasks.forEach(task => createTaskItem(task.title, task.id));
			generateInitialComment();  // Generate an initial comment after loading the tasks
		})
		.catch(error => console.error('Error:', error));

	// Add a new task
	addTaskBtn.addEventListener('click', () => {
		const taskText = taskInput.value.trim();
		if (taskText !== '') {
			// Create a new task on the server
			fetch('/tasks', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({
					title: taskText,
					description: '',
					due_date: '',
					priority: '',
				}),
			})
				.then(response => response.json())
				.then(data => {
					// Create a new task on the client side
					createTaskItem(taskText, data.id);
					console.log('Success:', data);
					updateTasks();
				})
				.catch((error) => console.error('Error:', error));

			taskInput.value = '';
		}
	});

	// Function to update the tasks and generate a sarcastic comment
	function updateTasks() {
		// Get the current state of the tasks
		const currentTasks = Array.from(taskList.children).map(li => li.textContent.slice(0, -1));

		// Delay the update by 1 second
		setTimeout(() => {
			// Call the /generate_comment endpoint with the old and new tasks
			fetch('/generate_comment', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({
					before: oldTasks,
					after: currentTasks,
				}),
			})
				.then(response => response.json())
				.then(data => {
					// Create a new comment element
					const newComment = document.createElement('p');
					newComment.textContent = data.comment;

					// Add the new comment to the top of the comment box
					commentBox.prepend(newComment);

					// If there are more than 5 comments, remove the oldest one
					if (commentBox.children.length > 5) {
						commentBox.removeChild(commentBox.lastChild);
					}				})
				.catch((error) => console.error('Error:', error));

			// Update the old tasks to the current tasks
			oldTasks = currentTasks;
		}, 100);
	}

	// Function to generate a comment about the current state of the task list
	function generateInitialComment() {
		// Get the current state of the tasks
		const currentTasks = Array.from(taskList.children).map(li => li.textContent.slice(0, -1));

		// Call the /generate_comment endpoint with the current tasks
		fetch('/generate_comment', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({
				before: [],
				after: currentTasks,
			}),
		})
			.then(response => response.json())
			.then(data => {
				// Create a new comment element
				const newComment = document.createElement('p');
				newComment.textContent = data.comment;

				// Add the new comment to the top of the comment box
				commentBox.prepend(newComment);
			})
			.catch((error) => console.error('Error:', error));
	}

	// Initialize the old tasks
	let oldTasks = Array.from(taskList.children).map(li => li.textContent.slice(0, -1)); 
});
