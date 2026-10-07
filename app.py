# app.py - Main Flask Application for TaskFlow

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# 1. Create the Flask app instance
app = Flask(__name__)

# 2. Configure the application
# Secret key is used for session management (flash messages, etc.)
app.config['SECRET_KEY'] = 'taskflow-secret-key-2024'

# 3. Configure SQLite database
# Basedir is the directory where app.py lives
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 4. Initialize the database
db = SQLAlchemy(app)

# 5. Define the Tasks model (database table structure)
class Task(db.Model):
    __tablename__ = 'tasks'
    
    # Columns/Fields
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), default='Other')
    priority = db.Column(db.String(20), default='Medium')
    status = db.Column(db.String(20), default='Pending')
    due_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    # Constructor for creating new tasks
    def __init__(self, title, description=None, category='Other', 
                 priority='Medium', status='Pending', due_date=None):
        self.title = title
        self.description = description
        self.category = category
        self.priority = priority
        self.status = status
        self.due_date = due_date
    
    # String representation (useful for debugging)
    def __repr__(self):
        return f'<Task {self.title}>'

# 6. Create the dashboard route
@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Dashboard route - Shows the main page with statistics.
    
    What this does:
    - Queries the database for task statistics
    - Handles sorting and overdue calculation
    - Passes the data to the template
    """
    # Get sort parameter (default: due_date ascending)
    sort_by = request.args.get('sort_by', 'due_date')
    sort_order = request.args.get('sort_order', 'asc')
    
    # Valid sort fields
    valid_sort_fields = ['due_date', 'priority', 'created_at', 'status']
    if sort_by not in valid_sort_fields:
        sort_by = 'due_date'
    if sort_order not in ['asc', 'desc']:
        sort_order = 'asc'
    
    # Calculate statistics from the database
    total_tasks = Task.query.count()
    
    # Count completed tasks (status = 'Completed')
    completed_tasks = Task.query.filter_by(status='Completed').count()
    
    # Count pending tasks (status = 'Pending')
    pending_tasks = Task.query.filter_by(status='Pending').count()
    
    # Count in-progress tasks
    in_progress_tasks = Task.query.filter_by(status='In Progress').count()
    
    # Calculate overdue tasks
    # A task is overdue if: due_date < today AND status != 'Completed'
    from datetime import date
    today = date.today()
    overdue_tasks = Task.query.filter(
        (Task.due_date < today) & 
        (Task.status != 'Completed')
    ).count()
    
    # Calculate completion percentage
    if total_tasks > 0:
        completion_percentage = round((completed_tasks / total_tasks) * 100)
    else:
        completion_percentage = 0
    
    # Enhanced: Tasks by Category (using SQL GROUP BY)
    tasks_by_category = db.session.query(
        Task.category, db.func.count(Task.id)
    ).group_by(Task.category).all()
    # Convert to dict for easy template access: {'Work': 5, 'Personal': 3, ...}
    category_counts = {category: count for category, count in tasks_by_category}
    # Ensure all expected categories are present even if count is 0
    for cat in ['Work', 'Personal', 'Learning', 'Shopping', 'Other']:
        if cat not in category_counts:
            category_counts[cat] = 0
    
    # Enhanced: Tasks by Priority (using SQL GROUP BY)
    tasks_by_priority = db.session.query(
        Task.priority, db.func.count(Task.id)
    ).group_by(Task.priority).all()
    # Convert to dict for easy template access: {'Low': 2, 'Medium': 5, ...}
    priority_counts = {priority: count for priority, count in tasks_by_priority}
    # Ensure all expected priorities are present even if count is 0
    for pri in ['Low', 'Medium', 'High']:
        if pri not in priority_counts:
            priority_counts[pri] = 0
    
    # Chart data: Tasks by Category (for bar chart)
    category_labels = ['Work', 'Personal', 'Learning', 'Shopping', 'Other']
    category_data = [category_counts.get(cat, 0) for cat in category_labels]
    
    # Chart data: Tasks completed over time (for line chart)
    # Get completed tasks with completed_at date, grouped by date
    completed_tasks_query = db.session.query(
        db.func.date(Task.completed_at), db.func.count(Task.id)
    ).filter(Task.status == 'Completed', Task.completed_at != None).group_by(db.func.date(Task.completed_at)).all()
    
    completion_dates = [str(row[0]) for row in completed_tasks_query]
    completion_counts = [row[1] for row in completed_tasks_query]
    
    # If no completion data, provide empty arrays
    if not completion_dates:
        completion_dates = []
        completion_counts = []
    
    # Apply sorting to task query
    # Build the ORDER BY clause dynamically
    sort_column = getattr(Task, sort_by, Task.due_date)
    if sort_order == 'desc':
        tasks = Task.query.order_by(sort_column.desc()).all()
    else:
        tasks = Task.query.order_by(sort_column.asc()).all()
    
    # Pass all statistics and sort info to the template
    return render_template(
        'index.html',
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        in_progress_tasks=in_progress_tasks,
        overdue_tasks=overdue_tasks,
        completion_percentage=completion_percentage,
        category_counts=category_counts,
        priority_counts=priority_counts,
        category_labels=category_labels,
        category_data=category_data,
        completion_dates=completion_dates,
        completion_counts=completion_counts,
        sort_by=sort_by,
        sort_order=sort_order,
        valid_sort_fields=valid_sort_fields,
        today=today
    )

# 7. API route to get all tasks (for JavaScript to consume)
@app.route('/api/tasks')
def get_tasks():
    """
    API endpoint that returns all tasks as JSON.
    Used by the frontend JavaScript to display the task list.
    """
    tasks = Task.query.all()
    
    # Convert each task to a dictionary
    task_list = []
    for task in tasks:
        task_dict = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'category': task.category,
            'priority': task.priority,
            'status': task.status,
            'due_date': task.due_date.strftime('%Y-%m-%d') if task.due_date else None,
            'created_at': task.created_at.strftime('%Y-%m-%d') if task.created_at else None,
            'completed_at': task.completed_at.strftime('%Y-%m-%d') if task.completed_at else None,
        }
        task_list.append(task_dict)
    
    return jsonify({'tasks': task_list, 'total': len(task_list)})

# 8. Route to add a new task
@app.route('/add', methods=['GET', 'POST'])
def add_task():
    """
    Add task route - Handles creating new tasks.
    GET: Shows the add task form
    POST: Processes the form data and saves to database
    """
    if request.method == 'POST':
        # Get form data
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category', 'Other')
        priority = request.form.get('priority', 'Medium')
        status = request.form.get('status', 'Pending')
        due_date_str = request.form.get('due_date')
        
        # Validation: title cannot be empty
        if not title or title.strip() == '':
            flash('Task title is required!', 'error')
            return redirect(url_for('add_task'))
        
        # Parse due date if provided
        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            except ValueError:
                flash('Invalid date format! Use YYYY-MM-DD.', 'error')
                return redirect(url_for('add_task'))
        
        # Create new task
        new_task = Task(
            title=title,
            description=description if description else None,
            category=category,
            priority=priority,
            status=status,
            due_date=due_date
        )
        
        # Add to database
        db.session.add(new_task)
        db.session.commit()
        
        flash('Task added successfully!', 'success')
        return redirect(url_for('index'))
    
    # GET request - show the form
    return render_template('add_task.html')

# 9. Route to edit a task
@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    """
    Edit task route - Handles updating existing tasks.
    GET: Shows the edit form pre-filled with current data
    POST: Either saves changes or deletes the task based on button clicked
    """
    # Find the task or return 404 if not found
    task = Task.query.get_or_404(task_id)
    
    if request.method == 'POST':
        # Check which button was clicked
        action = request.form.get('action')
        
        # Handle Delete
        if action == 'delete':
            db.session.delete(task)
            db.session.commit()
            flash('Task deleted successfully!', 'success')
            return redirect(url_for('index'))
        
        # Handle Save (default edit behavior)
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category', 'Other')
        priority = request.form.get('priority', 'Medium')
        status = request.form.get('status', 'Pending')
        due_date_str = request.form.get('due_date')
        
        # Validation: title cannot be empty
        if not title or title.strip() == '':
            flash('Task title is required!', 'error')
            return redirect(url_for('edit_task', task_id=task_id))
        
        # Parse due date if provided
        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            except ValueError:
                flash('Invalid date format! Use YYYY-MM-DD.', 'error')
                return redirect(url_for('edit_task', task_id=task_id))
        
        # Update task fields
        task.title = title
        task.description = description if description else None
        task.category = category
        task.priority = priority
        task.status = status
        task.due_date = due_date
        
        # Save to database
        db.session.commit()
        
        flash('Task updated successfully!', 'success')
        return redirect(url_for('index'))
    
    # GET request - show the form with current task data
    return render_template('edit_task.html', task=task)

# 10. Route to delete a task
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    """
    Delete task route - Removes a task from the database.
    Shows confirmation concept (though true confirmation requires JavaScript).
    """
    # Find the task or return 404
    task = Task.query.get_or_404(task_id)
    
    # Remove from database
    db.session.delete(task)
    db.session.commit()
    
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('index'))

# 11. Route to mark a task as completed
@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    """
    Complete task route - Marks a task as completed.
    Updates status and stores completion date.
    """
    # Find the task or return 404
    task = Task.query.get_or_404(task_id)
    
    # Update status to Completed
    task.status = 'Completed'
    
    # Store the completion date/time
    task.completed_at = datetime.utcnow()
    
    # Save to database
    db.session.commit()
    
    flash('Task marked as completed!', 'success')
    return redirect(url_for('index'))

# 12. Route for search/filter
@app.route('/search')
def search_tasks():
    """
    Search route - Filters tasks based on query parameters.
    ?q=search_term searches in title and description
    ?category=Work filters by category
    ?priority=High filters by priority
    ?status=Pending filters by status
    """
    # Get query parameters
    query = request.args.get('q', '', type=str)
    category = request.args.get('category', '', type=str)
    priority = request.args.get('priority', '', type=str)
    status = request.args.get('status', '', type=str)
    
    # Start with all tasks
    tasks_query = Task.query
    
    # Apply search filter (title or description contains the query)
    if query:
        tasks_query = tasks_query.filter(
            (Task.title.contains(query)) | (Task.description.contains(query))
        )
    
    # Apply category filter
    if category and category != 'All':
        tasks_query = tasks_query.filter_by(category=category)
    
    # Apply priority filter
    if priority and priority != 'All':
        tasks_query = tasks_query.filter_by(priority=priority)
    
    # Apply status filter
    if status and status != 'All':
        tasks_query = tasks_query.filter_by(status=status)
    
    # Execute query and get results
    tasks = tasks_query.all()
    
    return jsonify({
        'tasks': [{'id': t.id, 'title': t.title, 'status': t.status} for t in tasks],
        'total': len(tasks)
    })

# 13. Error handler for 404
@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 page"""
    return render_template('index.html'), 404

# 14. Initialize the database and run the app
if __name__ == '__main__':
    # Create the database tables (only runs once on first start)
    with app.app_context():
        db.create_all()
    
    # Run the Flask development server
    # debug=True enables auto-reloading and debug mode
    app.run(debug=True, host='127.0.0.1', port=5000)