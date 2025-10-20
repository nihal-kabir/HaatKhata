
import psycopg2
import psycopg2.extras
import os
import time
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from contextlib import contextmanager
from dotenv import load_dotenv
from urllib.parse import urlparse

# Load environment variables from .env file
load_dotenv()

# Database configuration from environment variables
# Support both DATABASE_URL (Render/NeonDB) and individual params (local development)
DATABASE_URL = os.getenv("DATABASE_URL")
DB_RETRY_SECONDS = int(os.getenv("DB_RETRY_SECONDS", 2))
DB_RETRY_MAX = int(os.getenv("DB_RETRY_MAX", 10))

if DATABASE_URL:
    # Parse DATABASE_URL for production (Render + NeonDB)
    parsed = urlparse(DATABASE_URL)
    DB_HOST = parsed.hostname
    DB_PORT = parsed.port or 5432
    DB_USER = parsed.username
    DB_PASS = parsed.password
    DB_NAME = parsed.path[1:]  # Remove leading '/'
else:
    # Use individual environment variables for local development
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", 5432))
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASS = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "task_manager_db")

class DatabaseManager:
    """Manages database connections and operations with retry logic"""

    def __init__(self):
        self.host = DB_HOST
        self.port = DB_PORT
        self.user = DB_USER
        self.password = DB_PASS
        self.database = DB_NAME

    @contextmanager
    def get_connection(self):
        """Context manager for database connections with retry logic"""
        last_exc = None
        for attempt in range(1, DB_RETRY_MAX + 1):
            try:
                # Build connection parameters
                conn_params = {
                    'host': self.host,
                    'port': self.port,
                    'user': self.user,
                    'password': self.password,
                    'dbname': self.database,
                    'connect_timeout': 10
                }

                # Add SSL for production (NeonDB requires SSL)
                if DATABASE_URL or os.getenv('FLASK_ENV') == 'production':
                    conn_params['sslmode'] = 'require'

                connection = psycopg2.connect(**conn_params)
                connection.autocommit = True
                try:
                    yield connection
                finally:
                    connection.close()
                return
            except Exception as e:
                last_exc = e
                print(f"DB connection attempt {attempt}/{DB_RETRY_MAX} failed: {e}")
                if attempt < DB_RETRY_MAX:
                    time.sleep(DB_RETRY_SECONDS)

        # If we get here all retries failed — raise the last exception
        raise last_exc
    
    def execute_query(self, query, params=None, fetch=False, fetch_all=True):
        """Execute SQL query and return results"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(query, params or ())
                if fetch:
                    if fetch_all:
                        results = cursor.fetchall()
                        return [dict(row) for row in results] if results else []
                    else:
                        result = cursor.fetchone()
                        return dict(result) if result else None
                else:
                    # For INSERT queries with RETURNING clause, fetch the returned ID
                    try:
                        result = cursor.fetchone()
                        if result and 'id' in result:
                            return result['id']
                    except:
                        pass
                    return None
    
    def init_database(self):
        """Initialize database tables"""
        # Create users table
        users_table = """
        CREATE TABLE IF NOT EXISTS "user" (
            id SERIAL PRIMARY KEY,
            username VARCHAR(80) UNIQUE NOT NULL,
            email VARCHAR(120) UNIQUE NOT NULL,
            password_hash VARCHAR(255),
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """

        # Create categories table
        categories_table = """
        CREATE TABLE IF NOT EXISTS category (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            description TEXT,
            color VARCHAR(7) DEFAULT '#007bff',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """

        # Create tasks table
        tasks_table = """
        CREATE TABLE IF NOT EXISTS task (
            id SERIAL PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            description TEXT,
            status VARCHAR(20) DEFAULT 'pending',
            priority VARCHAR(10) DEFAULT 'medium',
            due_date TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id INT NOT NULL,
            category_id INT,
            FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE CASCADE,
            FOREIGN KEY (category_id) REFERENCES category(id) ON DELETE SET NULL
        )
        """

        # Create trigger for updated_at
        trigger_sql = """
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ language 'plpgsql';

        DROP TRIGGER IF EXISTS update_task_updated_at ON task;
        CREATE TRIGGER update_task_updated_at BEFORE UPDATE ON task
        FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
        """
        
        # Execute table creation
        self.execute_query(users_table)
        self.execute_query(categories_table)
        self.execute_query(tasks_table)
        self.execute_query(trigger_sql)
        
        # Insert default categories if they don't exist
        default_categories = [
            ('Work', 'Work-related tasks', '#007bff'),
            ('Personal', 'Personal tasks and activities', '#28a745'),
            ('Shopping', 'Shopping lists and errands', '#ffc107'),
            ('Health', 'Health and fitness goals', '#dc3545'),
            ('Learning', 'Educational and skill development', '#6f42c1'),
        ]
        
        # Check if categories exist
        existing_count = self.execute_query(
            "SELECT COUNT(*) as count FROM category", 
            fetch=True, 
            fetch_all=False
        )
        
        if existing_count['count'] == 0:
            for name, desc, color in default_categories:
                self.execute_query(
                    "INSERT INTO category (name, description, color) VALUES (%s, %s, %s)",
                    (name, desc, color)
                )

# Initialize database manager
db_manager = DatabaseManager()

class User:
    """User model with raw SQL operations"""
    
    def __init__(self, id=None, username=None, email=None, password_hash=None, 
                 first_name=None, last_name=None, created_at=None):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name
        
        # Convert created_at string to datetime object if it's a string
        if isinstance(created_at, str):
            try:
                self.created_at = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                self.created_at = None
        else:
            self.created_at = created_at
    
    @classmethod
    def create(cls, username, email, password, first_name, last_name):
        """Create a new user"""
        password_hash = generate_password_hash(password)
        query = """
        INSERT INTO "user" (username, email, password_hash, first_name, last_name)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
        """
        user_id = db_manager.execute_query(
            query,
            (username, email, password_hash, first_name, last_name)
        )
        return cls.get_by_id(user_id)
    
    @classmethod
    def get_by_id(cls, user_id):
        """Get user by ID"""
        query = 'SELECT * FROM "user" WHERE id = %s'
        result = db_manager.execute_query(query, (user_id,), fetch=True, fetch_all=False)
        if result:
            return cls(**result)
        return None

    @classmethod
    def get_by_username(cls, username):
        """Get user by username"""
        query = 'SELECT * FROM "user" WHERE username = %s'
        result = db_manager.execute_query(query, (username,), fetch=True, fetch_all=False)
        if result:
            return cls(**result)
        return None

    @classmethod
    def get_by_email(cls, email):
        """Get user by email"""
        query = 'SELECT * FROM "user" WHERE email = %s'
        result = db_manager.execute_query(query, (email,), fetch=True, fetch_all=False)
        if result:
            return cls(**result)
        return None
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def update(self, **kwargs):
        """Update user fields"""
        fields = []
        values = []
        for key, value in kwargs.items():
            if hasattr(self, key):
                fields.append(f"{key} = %s")
                values.append(value)
                setattr(self, key, value)

        if fields:
            values.append(self.id)
            query = f'UPDATE "user" SET {", ".join(fields)} WHERE id = %s'
            db_manager.execute_query(query, values)
    
    # Flask-Login required methods
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)

class Category:
    """Category model with raw SQL operations"""
    
    def __init__(self, id=None, name=None, description=None, color=None, created_at=None):
        self.id = id
        self.name = name
        self.description = description
        self.color = color
        
        # Convert created_at string to datetime object if it's a string
        if isinstance(created_at, str):
            try:
                self.created_at = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                self.created_at = None
        else:
            self.created_at = created_at
    
    @classmethod
    def create(cls, name, description=None, color='#007bff'):
        """Create a new category"""
        query = """
        INSERT INTO category (name, description, color)
        VALUES (%s, %s, %s)
        RETURNING id
        """
        category_id = db_manager.execute_query(query, (name, description, color))
        return cls.get_by_id(category_id)
    
    @classmethod
    def get_by_id(cls, category_id):
        """Get category by ID"""
        query = "SELECT * FROM category WHERE id = %s"
        result = db_manager.execute_query(query, (category_id,), fetch=True, fetch_all=False)
        if result:
            return cls(**result)
        return None
    
    @classmethod
    def get_all(cls):
        """Get all categories"""
        query = "SELECT * FROM category ORDER BY name"
        results = db_manager.execute_query(query, fetch=True)
        return [cls(**row) for row in results]
    
    def update(self, **kwargs):
        """Update category fields"""
        fields = []
        values = []
        for key, value in kwargs.items():
            if hasattr(self, key):
                fields.append(f"{key} = %s")
                values.append(value)
                setattr(self, key, value)
        
        if fields:
            values.append(self.id)
            query = f"UPDATE category SET {', '.join(fields)} WHERE id = %s"
            db_manager.execute_query(query, values)
    
    def delete(self):
        """Delete category"""
        query = "DELETE FROM category WHERE id = %s"
        db_manager.execute_query(query, (self.id,))
    
    def get_tasks(self, user_id=None):
        """Get tasks associated with this category, optionally filtered by user"""
        query = """
        SELECT t.*, c.name as category_name, c.color as category_color
        FROM task t
        LEFT JOIN category c ON t.category_id = c.id
        WHERE t.category_id = %s
        """
        params = [self.id]

        if user_id is not None:
            query += " AND t.user_id = %s"
            params.append(user_id)

        query += " ORDER BY t.created_at DESC"

        results = db_manager.execute_query(query, params, fetch=True)
        return [Task(**row) for row in results] if results else []

    @property
    def tasks(self):
        """Get all tasks associated with this category (backward compatibility)"""
        return self.get_tasks()

class Task:
    """Task model with raw SQL operations"""
    
    def __init__(self, id=None, title=None, description=None, status='pending', 
                 priority='medium', due_date=None, created_at=None, updated_at=None,
                 user_id=None, category_id=None, category_name=None, category_color=None):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority
        
        # Convert datetime strings to datetime objects if they're strings
        if isinstance(due_date, str):
            try:
                self.due_date = datetime.strptime(due_date, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                try:
                    self.due_date = datetime.strptime(due_date, '%Y-%m-%d')
                except ValueError:
                    self.due_date = None
        else:
            self.due_date = due_date
            
        if isinstance(created_at, str):
            try:
                self.created_at = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                self.created_at = None
        else:
            self.created_at = created_at
            
        if isinstance(updated_at, str):
            try:
                self.updated_at = datetime.strptime(updated_at, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                self.updated_at = None
        else:
            self.updated_at = updated_at
            
        self.user_id = user_id
        self.category_id = category_id
        self.category_name = category_name
        self.category_color = category_color
    
    @classmethod
    def create(cls, title, user_id, description=None, status='pending',
               priority='medium', due_date=None, category_id=None):
        """Create a new task"""
        query = """
        INSERT INTO task (title, description, status, priority, due_date, user_id, category_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id
        """
        task_id = db_manager.execute_query(
            query,
            (title, description, status, priority, due_date, user_id, category_id)
        )
        return cls.get_by_id(task_id)
    
    @classmethod
    def get_by_id(cls, task_id):
        """Get task by ID with category info"""
        query = """
        SELECT t.*, c.name as category_name, c.color as category_color
        FROM task t
        LEFT JOIN category c ON t.category_id = c.id
        WHERE t.id = %s
        """
        result = db_manager.execute_query(query, (task_id,), fetch=True, fetch_all=False)
        if result:
            return cls(**result)
        return None
    
    @classmethod
    def get_by_user(cls, user_id, status=None, category_id=None, search=None):
        """Get tasks by user with optional filters"""
        query = """
        SELECT t.*, c.name as category_name, c.color as category_color
        FROM task t
        LEFT JOIN category c ON t.category_id = c.id
        WHERE t.user_id = %s
        """
        params = [user_id]
        
        if status:
            query += " AND t.status = %s"
            params.append(status)
        
        if category_id:
            query += " AND t.category_id = %s"
            params.append(category_id)
        
        if search:
            query += " AND (t.title LIKE %s OR t.description LIKE %s)"
            search_term = f"%{search}%"
            params.extend([search_term, search_term])
        
        query += " ORDER BY t.created_at DESC"
        
        results = db_manager.execute_query(query, params, fetch=True)
        return [cls(**row) for row in results]
    
    @classmethod
    def get_stats_by_user(cls, user_id):
        """Get task statistics for user"""
        query = """
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending,
            SUM(CASE WHEN status = 'in_progress' THEN 1 ELSE 0 END) as in_progress,
            SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
            SUM(CASE WHEN due_date < NOW() AND status != 'completed' THEN 1 ELSE 0 END) as overdue
        FROM task 
        WHERE user_id = %s
        """
        result = db_manager.execute_query(query, (user_id,), fetch=True, fetch_all=False)
        return result or {'total': 0, 'pending': 0, 'in_progress': 0, 'completed': 0, 'overdue': 0}
    
    def update(self, **kwargs):
        """Update task fields"""
        fields = []
        values = []
        for key, value in kwargs.items():
            if hasattr(self, key) and key not in ['id', 'created_at', 'category_name', 'category_color']:
                fields.append(f"{key} = %s")
                values.append(value)
                setattr(self, key, value)
        
        if fields:
            values.append(self.id)
            query = f"UPDATE task SET {', '.join(fields)}, updated_at = NOW() WHERE id = %s"
            db_manager.execute_query(query, values)
    
    def delete(self):
        """Delete task"""
        query = "DELETE FROM task WHERE id = %s"
        db_manager.execute_query(query, (self.id,))
    
    @property
    def is_overdue(self):
        """Check if task is overdue"""
        if self.due_date and self.status != 'completed':
            return self.due_date < datetime.now()
        return False
    
    @property
    def category(self):
        """Return a category-like object with name and color"""
        if self.category_name:
            class CategoryLike:
                def __init__(self, name, color):
                    self.name = name
                    self.color = color
            return CategoryLike(self.category_name, self.category_color)
        return None
    
    @property
    def status_color(self):
        """Return color based on status"""
        colors = {
            'pending': 'warning',
            'in_progress': 'info', 
            'completed': 'success'
        }
        return colors.get(self.status, 'secondary')
    
    @property
    def priority_color(self):
        """Return color based on priority"""
        colors = {
            'low': 'success',
            'medium': 'warning',
            'high': 'danger'
        }
        return colors.get(self.priority, 'secondary')
