# TaskFlow — Smart Todo & Task Management App

## Project Description
TaskFlow is a modern, professional Todo and Task Management Web Application built with a full-stack approach using Python Flask, SQLite, and HTML/CSS/JavaScript. It helps individuals organize their tasks, track productivity, and manage daily workflows efficiently.

The application features a clean, responsive dashboard with statistics, search and filtering capabilities, sorting options, and analytics charts powered by Chart.js. All data is stored in a SQLite database, and the application follows CRUD (Create, Read, Update, Delete) principles.

## Features

### Core Functionality
- **Dashboard**: Overview of total tasks, completed, pending, overdue tasks, and completion percentage
- **Add Task**: Create tasks with title, description, category, priority, due date, and status
- **Task List**: Display all tasks with full details and action buttons
- **Edit Task**: Modify existing task details
- **Delete Task**: Remove tasks with confirmation
- **Mark as Completed**: Update task status and track completion date

### Search & Filters
- Search tasks by title or description
- Filter by: All/Pending/In Progress/Completed/Overdue status
- Filter by: Work/Personal/Learning/Shopping/Other categories
- Filter by: Low/Medium/High priority
- Sort by: Due date, Priority, Created date, Status

### Analytics & Visualization
- Doughnut chart: Completed vs Pending tasks
- Bar chart: Tasks by Category
- Line chart: Tasks completed over time

### Responsive Design
- Works on desktop, laptop, tablet, and mobile devices
- Mobile-friendly navigation with hamburger menu
- Clean, professional UI that adapts to any screen size

## Tech Stack

### Frontend
- HTML5
- CSS3 (with responsive design and custom properties)
- Vanilla JavaScript (no frameworks)

### Backend
- Python 3.x
- Flask (web framework)

### Database
- SQLite (file-based, no separate server needed)

### Visualization
- Chart.js (for analytics charts)

## Database Structure

### Tasks Table

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary key, auto-increment |
| `title` | VARCHAR(100) | Task title (required) |
| `description` | TEXT | Optional task description |
| `category` | VARCHAR(50) | Task category (default: 'Other') |
| `priority` | VARCHAR(20) | Priority level (default: 'Medium') |
| `status` | VARCHAR(20) | Task status (default: 'Pending') |
| `due_date` | DATETIME | Task due date (optional) |
| `created_at` | DATETIME | Timestamp when task was created |
| `completed_at` | DATETIME | Timestamp when task was completed (nullable) |

### Sample SQL Queries

```sql
-- Count total tasks
SELECT COUNT(*) FROM tasks;

-- Count completed tasks
SELECT COUNT(*) FROM tasks WHERE status = 'Completed';

-- Count pending tasks
SELECT COUNT(*) FROM tasks WHERE status = 'Pending';

-- Count overdue tasks
SELECT COUNT(*) FROM tasks 
WHERE due_date < date('now') 
AND status != 'Completed';

-- Tasks by category
SELECT category, COUNT(*) FROM tasks GROUP BY category;

-- Tasks by priority
SELECT priority, COUNT(*) FROM tasks GROUP BY priority;

-- Latest tasks
SELECT * FROM tasks ORDER BY created_at DESC LIMIT 5;

-- Tasks due within 7 days
SELECT * FROM tasks 
WHERE due_date BETWEEN date('now') AND date('now', '+7 days')
AND status != 'Completed';
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Steps

1. **Clone the repository** (or download the project files):
   ```bash
   git clone https://github.com/yourusername/TaskFlow.git
   cd TaskFlow
   ```

2. **Create a Python virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows PowerShell:
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - On Windows Command Prompt:
     ```cmd
     venv\Scripts\activate.bat
     ```
   - On macOS / Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**:
   ```bash
   python app.py
   ```

6. **Open your web browser** and visit:
   ```
   http://127.0.0.1:5000
   ```

### Requirements.txt
```
Flask==3.0.3
Flask-SQLAlchemy==3.1.1
```

## How to Use

### Basic Workflow

1. **View Dashboard**: Upon starting the app, you'll see the dashboard with statistics and task list
2. **Add a New Task**: Click "Add New Task" to open the task form
3. **Fill in Task Details**:
   - Enter a required Task Title
   - optionally add Description, Category, Priority, Status, and Due Date
   - Click "Add Task"
4. **Manage Tasks**:
   - **Edit**: Click the pencil icon on any task card
   - **Complete**: Click the checkmark icon to mark a task as completed
   - **Delete**: Click the trash icon (confirmation popup appears)
5. **Use Filters and Search**:
   - Use the filter controls at the top to narrow down tasks
   - Search by typing in the search box
   - Sort by different fields using the sort dropdown
6. **View Analytics**: Scroll down to see productivity charts

### Example Tasks

| Title | Category | Priority | Due Date | Status |
|-------|----------|----------|----------|--------|
| Finish Project Report | Work | High | 2024-01-15 | Pending |
| Buy Groceries | Shopping | Medium | 2024-01-10 | Pending |
| Learn Python Basics | Learning | High | 2023-12-20 | Pending |
| Call Mom | Personal | Low | 2024-01-05 | Completed |
| Pay Electricity Bill | Personal | Medium | 2023-12-25 | Overdue |

## Screenshots

![TaskFlow Dashboard](screenshots/dashboard-desktop.png)
*Figure 1: TaskFlow Dashboard on desktop*

![TaskFlow Mobile](screenshots/dashboard-mobile.png)
*Figure 2: TaskFlow Dashboard on mobile*

*(Add screenshots of your application by running the app, pressing Print Screen, and adding the images to a `screenshots/` folder)*

## Future Improvements

Potential enhancements for future versions:

- **User Authentication**: Implement login system for multiple users
- **PostgreSQL**: Migrate from SQLite to PostgreSQL for production use
- **REST API**: Expose API endpoints for mobile apps or third-party integrations
- **Email Reminders**: Send email notifications for due tasks
- **Recurring Tasks**: Support tasks that repeat daily/weekly/monthly
- **Task Export**: Export tasks to CSV/Excel format
- **Dark Mode**: Add dark theme option
- **Calendar View**: Visual calendar for task due dates
- **Priority Reordering**: Drag-and-drop to reorder tasks by priority

## What I Learned

During the development of TaskFlow, I gained valuable experience in:

### Backend Development (Python & Flask)
- Setting up Flask applications with proper routing
- Designing SQLite database schemas with proper relationships
- Implementing CRUD operations (Create, Read, Update, Delete)
- Using Flask-SQLAlchemy for database interactions
- Creating RESTful API endpoints
- Handling form validation and user input
- Managing database sessions and transactions
- Implementing overdue logic with date comparisons
- Calculating aggregate statistics with SQL GROUP BY

### Frontend Development (HTML/CSS/JavaScript)
- Creating responsive layouts that work on mobile and desktop
- Designing clean, professional UI with consistent styling
- Implementing micro-interactions and focus states
- Using CSS Grid and Flexbox for layout
- Adding accessibility features (skip links, focus states)
- Integrating Chart.js for data visualization
- Managing state between Flask backend and JavaScript frontend

### Full-Stack Integration
- How Flask routes communicate with HTML templates
- Passing data from Python to JavaScript via Jinja2
- Handling form submissions via POST/GET methods
- Using flash messages for user feedback
- Implementing redirect-after-post pattern
- Managing database relationships and queries

### Software Engineering Practices
- Building project structure with separated concerns
- Using virtual environments for dependency management
- Writing clean, documented code
- Testing core functionality
- Creating professional documentation (README.md)
- Planning feature implementation in phases
- Balancing complexity with beginner-friendly approach

---

## Quick Start Commands

```bash
# 1. Navigate to project
cd TaskFlow

# 2. Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install Flask Flask-SQLAlchemy

# 4. Run the app
python app.py

# 5. Open browser
http://127.0.0.1:5000
```