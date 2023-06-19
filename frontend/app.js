document.addEventListener('DOMContentLoaded', () => {
	const taskInput = document.getElementById('task-input');
	const addTaskBtn = document.getElementById('add-task-btn');
	const taskList = document.getElementById('task-list');
  
	addTaskBtn.addEventListener('click', () => {
	  const taskText = taskInput.value.trim();
	  if (taskText !== '') {
		const taskItem = document.createElement('li');
		taskItem.textContent = taskText;
		taskList.appendChild(taskItem);
		taskInput.value = '';
	  }
	});
  });
  