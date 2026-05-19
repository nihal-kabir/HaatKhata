from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from database import db_manager, User, Task, Category
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Template constants to avoid duplication
TEMPLATE_REGISTER = 'register.html'
TEMPLATE_LOGIN = 'login.html'
TEMPLATE_DASHBOARD = 'dashboard.html'
TEMPLATE_TASKS = 'tasks.html'
TEMPLATE_CREATE_TASK = 'create_task.html'
TEMPLATE_EDIT_TASK = 'edit_task.html'
TEMPLATE_CATEGORIES = 'categories.html'
TEMPLATE_PROFILE = 'profile.html'
TEMPLATE_INDEX = 'index.html'

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

# Database initialization - will be handled by init_db.py script during deployment
# Or you can call it manually in production

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

# Routes

@app.route('/')
def index():
    """Homepage - redirect to dashboard if logged in, otherwise show landing page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template(TEMPLATE_INDEX, app_name="HaatKhata")

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        
        # Check if user already exists
        if User.get_by_username(username):
            flash('Username already exists!', 'error')
            return render_template(TEMPLATE_REGISTER)
        
        if User.get_by_email(email):
            flash('Email already registered!', 'error')
            return render_template(TEMPLATE_REGISTER)
        
        # Create new user
        try:
            user = User.create(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash('Registration failed. Please try again.', 'error')
            return render_template(TEMPLATE_REGISTER)
    
    return render_template(TEMPLATE_REGISTER)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.get_by_username(username)
        
        if user and user.check_password(password):
            login_user(user)
            flash(f'Welcome back, {user.first_name}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!', 'error')
    
    return render_template(TEMPLATE_LOGIN)

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard with statistics"""
    # Get user's task statistics using raw SQL
    stats = Task.get_stats_by_user(current_user.id)
    
    # Get recent tasks
    recent_tasks = Task.get_by_user(current_user.id)[:5]  # Get first 5 tasks
    
    return render_template(TEMPLATE_DASHBOARD,
                         total_tasks=stats['total'],
                         completed_tasks=stats['completed'],
                         pending_tasks=stats['pending'],
                         in_progress_tasks=stats['in_progress'],
                         recent_tasks=recent_tasks,
                         overdue_tasks=stats['overdue'])

@app.route('/tasks')
@login_required
def tasks():
    """View all tasks with filtering"""
    # Get filter parameters
    status_filter = request.args.get('status', '')
    category_filter = request.args.get('category', '')
    priority_filter = request.args.get('priority', '')
    search_query = request.args.get('search', '')
    
    # Use raw SQL to get filtered tasks
    category_id = int(category_filter) if category_filter else None
    tasks = Task.get_by_user(
        user_id=current_user.id,
        status=status_filter if status_filter else None,
        category_id=category_id,
        search=search_query if search_query else None
    )
    
    # Filter by priority if specified
    if priority_filter:
        tasks = [task for task in tasks if task.priority == priority_filter]
    
    categories = Category.get_all()
    
    return render_template(TEMPLATE_TASKS, 
                         tasks=tasks, 
                         categories=categories,
                         current_status=status_filter,
                         current_category=category_filter,
                         current_priority=priority_filter,
                         current_search=search_query)

@app.route('/task/new', methods=['GET', 'POST'])
@login_required
def create_task():
    """Create new task"""
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        priority = request.form['priority']
        category_id = request.form.get('category_id') or None
        due_date_str = request.form.get('due_date')
        
        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            except ValueError:
                flash('Invalid date format!', 'error')
                return render_template(TEMPLATE_CREATE_TASK, categories=Category.get_all())
        
        try:
            task = Task.create(
                title=title,
                description=description,
                priority=priority,
                due_date=due_date,
                category_id=int(category_id) if category_id else None,
                user_id=current_user.id
            )
            flash('Task created successfully!', 'success')
            return redirect(url_for('tasks'))
        except Exception as e:
            flash('Failed to create task. Please try again.', 'error')
            return render_template(TEMPLATE_CREATE_TASK, categories=Category.get_all())
    
    categories = Category.get_all()
    return render_template(TEMPLATE_CREATE_TASK, categories=categories)

@app.route('/task/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    """Edit existing task"""
    task = Task.get_by_id(task_id)
    if not task or task.user_id != current_user.id:
        flash('Task not found!', 'error')
        return redirect(url_for('tasks'))
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        priority = request.form['priority']
        status = request.form['status']
        category_id = request.form.get('category_id') or None
        
        due_date = None
        due_date_str = request.form.get('due_date')
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            except ValueError:
                flash('Invalid date format!', 'error')
                return render_template(TEMPLATE_EDIT_TASK, task=task, categories=Category.get_all())
        
        try:
            task.update(
                title=title,
                description=description,
                priority=priority,
                status=status,
                category_id=int(category_id) if category_id else None,
                due_date=due_date
            )
            flash('Task updated successfully!', 'success')
            return redirect(url_for('tasks'))
        except Exception as e:
            flash('Failed to update task. Please try again.', 'error')
    
    categories = Category.get_all()
    return render_template(TEMPLATE_EDIT_TASK, task=task, categories=categories)

@app.route('/task/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    """Delete task"""
    task = Task.get_by_id(task_id)
    if not task or task.user_id != current_user.id:
        flash('Task not found!', 'error')
        return redirect(url_for('tasks'))
    
    try:
        task.delete()
        flash('Task deleted successfully!', 'success')
    except Exception as e:
        flash('Failed to delete task. Please try again.', 'error')
    
    return redirect(url_for('tasks'))

@app.route('/categories')
@login_required
def categories():
    """Manage categories"""
    categories = Category.get_all()
    return render_template(TEMPLATE_CATEGORIES, categories=categories)

@app.route('/category/new', methods=['POST'])
@login_required
def create_category():
    """Create new category"""
    name = request.form['name']
    description = request.form.get('description', '')
    color = request.form.get('color', '#007bff')
    
    try:
        category = Category.create(name=name, description=description, color=color)
        flash('Category created successfully!', 'success')
    except Exception as e:
        flash('Failed to create category. Please try again.', 'error')
    
    return redirect(url_for('categories'))

@app.route('/profile')
@login_required
def profile():
    """User profile"""
    return render_template(TEMPLATE_PROFILE, user=current_user)

@app.route('/profile/edit', methods=['POST'])
@login_required
def edit_profile():
    """Edit user profile"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    
    # Check if email is already taken by another user
    existing_user = User.get_by_email(email)
    if existing_user and existing_user.id != current_user.id:
        flash('Email already in use by another user!', 'error')
        return redirect(url_for('profile'))
    
    try:
        current_user.update(
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        flash('Profile updated successfully!', 'success')
    except Exception as e:
        flash('Failed to update profile. Please try again.', 'error')
    
    return redirect(url_for('profile'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)
