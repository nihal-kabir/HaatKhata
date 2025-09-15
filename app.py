from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from models import db, User, Task, Category
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import pymysql

# Install PyMySQL as MySQLdb for SQLAlchemy
pymysql.install_as_MySQLdb()

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
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///task_manager.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'error')
            return render_template(TEMPLATE_REGISTER)
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'error')
            return render_template(TEMPLATE_REGISTER)
        
        # Create new user
        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template(TEMPLATE_REGISTER)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
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
    # Get user's task statistics
    total_tasks = Task.query.filter_by(user_id=current_user.id).count()
    completed_tasks = Task.query.filter_by(user_id=current_user.id, status='completed').count()
    pending_tasks = Task.query.filter_by(user_id=current_user.id, status='pending').count()
    in_progress_tasks = Task.query.filter_by(user_id=current_user.id, status='in_progress').count()
    
    # Get recent tasks
    recent_tasks = Task.query.filter_by(user_id=current_user.id)\
                           .order_by(Task.created_at.desc())\
                           .limit(5).all()
    
    # Get overdue tasks
    overdue_tasks = Task.query.filter_by(user_id=current_user.id)\
                            .filter(Task.due_date < datetime.now())\
                            .filter(Task.status != 'completed')\
                            .count()
    
    return render_template(TEMPLATE_DASHBOARD,
                         total_tasks=total_tasks,
                         completed_tasks=completed_tasks,
                         pending_tasks=pending_tasks,
                         in_progress_tasks=in_progress_tasks,
                         recent_tasks=recent_tasks,
                         overdue_tasks=overdue_tasks)

@app.route('/tasks')
@login_required
def tasks():
    """View all tasks with filtering"""
    # Get filter parameters
    status_filter = request.args.get('status', '')
    category_filter = request.args.get('category', '')
    priority_filter = request.args.get('priority', '')
    search_query = request.args.get('search', '')
    
    # Build query
    query = Task.query.filter_by(user_id=current_user.id)
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    if category_filter:
        query = query.filter_by(category_id=category_filter)
    if priority_filter:
        query = query.filter_by(priority=priority_filter)
    if search_query:
        query = query.filter(Task.title.contains(search_query) | 
                           Task.description.contains(search_query))
    
    tasks = query.order_by(Task.created_at.desc()).all()
    categories = Category.query.all()
    
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
                due_date = datetime.strptime(due_date_str, '%Y-%m-%dT%H:%M')
            except ValueError:
                flash('Invalid date format!', 'error')
                return render_template(TEMPLATE_CREATE_TASK, categories=Category.query.all())
        
        task = Task(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            category_id=category_id,
            user_id=current_user.id
        )
        
        db.session.add(task)
        db.session.commit()
        
        flash('Task created successfully!', 'success')
        return redirect(url_for('tasks'))
    
    categories = Category.query.all()
    return render_template(TEMPLATE_CREATE_TASK, categories=categories)

@app.route('/task/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    """Edit existing task"""
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form['description']
        task.priority = request.form['priority']
        task.status = request.form['status']
        task.category_id = request.form.get('category_id') or None
        
        due_date_str = request.form.get('due_date')
        if due_date_str:
            try:
                task.due_date = datetime.strptime(due_date_str, '%Y-%m-%dT%H:%M')
            except ValueError:
                flash('Invalid date format!', 'error')
                return render_template(TEMPLATE_EDIT_TASK, task=task, categories=Category.query.all())
        else:
            task.due_date = None
        
        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('tasks'))
    
    categories = Category.query.all()
    return render_template(TEMPLATE_EDIT_TASK, task=task, categories=categories)

@app.route('/task/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    """Delete task"""
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('tasks'))

@app.route('/categories')
@login_required
def categories():
    """Manage categories"""
    categories = Category.query.all()
    return render_template(TEMPLATE_CATEGORIES, categories=categories)

@app.route('/category/new', methods=['POST'])
@login_required
def create_category():
    """Create new category"""
    name = request.form['name']
    description = request.form.get('description', '')
    color = request.form.get('color', '#007bff')
    
    category = Category(name=name, description=description, color=color)
    db.session.add(category)
    db.session.commit()
    
    flash('Category created successfully!', 'success')
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
    current_user.first_name = request.form['first_name']
    current_user.last_name = request.form['last_name']
    current_user.email = request.form['email']
    
    # Check if email is already taken by another user
    existing_user = User.query.filter_by(email=current_user.email).first()
    if existing_user and existing_user.id != current_user.id:
        flash('Email already in use by another user!', 'error')
        return redirect(url_for('profile'))
    
    db.session.commit()
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('profile'))

# Initialize database
with app.app_context():
    db.create_all()
    
    # Create default categories if they don't exist
    if not Category.query.first():
        default_categories = [
            Category(name='Work', description='Work-related tasks', color='#007bff'),
            Category(name='Personal', description='Personal tasks', color='#28a745'),
            Category(name='Shopping', description='Shopping lists', color='#ffc107'),
            Category(name='Health', description='Health and fitness', color='#dc3545'),
        ]
        for category in default_categories:
            db.session.add(category)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
