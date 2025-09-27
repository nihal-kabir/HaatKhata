# HaatKhata

A web-based task management application built with Flask, featuring user authentication, task organization with categories, and comprehensive task tracking capabilities.

## Overview

HaatKhata is a full-featured task management system that allows users to create, organize, and track their tasks efficiently. The application provides a clean, responsive interface for managing personal and professional tasks with advanced filtering and categorization options.

## Features

- **User Authentication**: Secure user registration and login system with password hashing
- **Task Management**: Complete CRUD operations for tasks with title, description, priority levels, and due dates
- **Categories**: Color-coded task categorization for better organization
- **Dashboard**: Visual overview with task statistics and recent activity
- **Advanced Filtering**: Search and filter tasks by status, category, priority, and keywords
- **Responsive Design**: Mobile-friendly interface built with Bootstrap 5
- **Database Integration**: MySQL database with proper foreign key relationships

## Technology Stack

- **Backend**: Flask 2.3.3, Python
- **Database**: MySQL with PyMySQL connector
- **Authentication**: Flask-Login with Werkzeug password hashing
- **Frontend**: HTML5, CSS3, Bootstrap 5, Jinja2 templating
- **Configuration**: Environment-based configuration with python-dotenv
- **Production**: Gunicorn WSGI server ready

## Database Schema

### Users Table
- User credentials and profile information
- Password hashing for security
- Relationship with tasks

### Categories Table
- Task categorization with custom colors
- Optional descriptions
- Many-to-many relationship with tasks

### Tasks Table
- Complete task information (title, description, status, priority)
- Due date tracking with overdue detection
- Foreign key relationships to users and categories
- Automatic timestamp management

## Installation

1. Clone the repository:
```bash
git clone https://github.com/nihal-kabir/HaatKhata.git
cd HaatKhata
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
```
Edit `.env` with your database configuration:
- `DB_HOST`: MySQL server host
- `DB_USER`: Database username  
- `DB_PASSWORD`: Database password
- `DB_NAME`: Database name
- `SECRET_KEY`: Flask application secret key

5. Initialize the database:
The application automatically creates necessary tables on first run.

6. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Application Routes

### Authentication
- `/` - Landing page (redirects to dashboard if authenticated)
- `/register` - User registration
- `/login` - User authentication
- `/logout` - User logout

### Core Features
- `/dashboard` - Task overview and statistics
- `/tasks` - Task list with filtering options
- `/task/new` - Create new task
- `/task/<id>/edit` - Edit existing task
- `/task/<id>/delete` - Delete task
- `/categories` - Category management
- `/profile` - User profile management

## Project Structure

```
HaatKhata/
├── app.py                 # Main Flask application with all routes
├── database.py            # Database models and operations (raw SQL)
├── models.py              # SQLAlchemy model definitions
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── static/
│   ├── css/style.css     # Custom styling
│   └── js/main.js        # Client-side JavaScript
└── templates/            # Jinja2 HTML templates
    ├── base.html         # Base template with navigation
    ├── dashboard.html    # Dashboard with statistics
    ├── tasks.html        # Task listing and filtering
    ├── create_task.html  # Task creation form
    ├── edit_task.html    # Task editing form
    ├── categories.html   # Category management
    ├── profile.html      # User profile
    ├── login.html        # Login form
    ├── register.html     # Registration form
    └── index.html        # Landing page
```

## Development Notes

- The application uses raw SQL queries through PyMySQL for database operations
- SQLAlchemy models are included but not actively used in the current implementation
- Datetime handling includes proper string-to-datetime conversion for database compatibility
- Template safety measures prevent errors when datetime fields are null
- Bootstrap 5 provides responsive design and modern UI components

## Security Features

- Password hashing using Werkzeug's security utilities
- Session-based authentication with Flask-Login
- CSRF protection through proper form handling
- Environment variable configuration for sensitive data

## Production Deployment

The application includes Gunicorn for production deployment. Key considerations:

- Set `FLASK_ENV=production` in environment variables
- Use a reverse proxy (nginx) for static file serving
- Configure proper MySQL connection pooling
- Set up proper logging and monitoring

## License

This project is open source and available under the MIT License.