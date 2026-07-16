let draggedElement = null;

const taskList = document.getElementById('taskList');
const taskItems = document.querySelectorAll('.task-item');

taskItems.forEach(item => {
item.addEventListener('dragstart', function() {
    draggedElement = this;
    this.classList.add('dragging');
});

item.addEventListener('dragend', function() {
    this.classList.remove('dragging');
    taskItems.forEach(i => i.classList.remove('drag-over'));
    draggedElement = null;
});

item.addEventListener('dragover', function(e) {
    e.preventDefault();
    if (this !== draggedElement) {
    this.classList.add('drag-over');
    }
});

item.addEventListener('dragleave', function() {
    this.classList.remove('drag-over');
});

item.addEventListener('drop', function(e) {
    e.preventDefault();
    if (this !== draggedElement) {
    // Swap elements
    if (draggedElement.compareDocumentPosition(this) === Node.DOCUMENT_POSITION_FOLLOWING) {
        this.parentNode.insertBefore(draggedElement, this);
    } else {
        this.parentNode.insertBefore(draggedElement, this.nextSibling);
    }
    
    // Save new order to server
    saveTaskOrder();
    }
    this.classList.remove('drag-over');
});
});

function saveTaskOrder() {
const taskItems = document.querySelectorAll('.task-item');
const taskIds = Array.from(taskItems).map(item => item.getAttribute('data-task-id'));

fetch('{% url "update_order" %}', {
    method: 'POST',
    headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({
    task_ids: taskIds
    })
})
.then(response => response.json())
.then(data => {
    if (data.status === 'success') {
    console.log('Task order updated successfully');
    }
})
.catch(error => console.error('Error:', error));
}

function getCookie(name) {
let cookieValue = null;
if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i].trim();
    if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
    }
    }
}
return cookieValue;
}