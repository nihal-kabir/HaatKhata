# HaatKhata

> **কাজ শেষ, খাতা ফাঁকা** - A modern task management web application built with Flask

[![Live Demo](https://img.shields.io/badge/Live%20Demo-haatkhata--37ry.onrender.com-brightgreen?style=for-the-badge)](https://haatkhata-37ry.onrender.com)

## Overview

HaatKhata is a comprehensive task management system that enables users to create, organize, and track tasks efficiently. Built with Flask and featuring a clean, responsive interface, it provides advanced filtering and categorization options for both personal and professional use.

## Key Features

- **Secure Authentication** - User registration and login with password hashing
- **Task Management** - Complete CRUD operations with priority levels and due dates
- **Smart Categories** - Color-coded task organization with custom categories
- **Dashboard Analytics** - Visual overview with task statistics and recent activity
- **Advanced Filtering** - Search and filter by status, category, priority, and keywords
- **Responsive Design** - Mobile-friendly interface built with Bootstrap 5
- **Robust Database** - MySQL/PostgreSQL support with proper relationships

## Live Demo

**[View Live Application →](https://haatkhata-37ry.onrender.com)**

Test the application with full functionality including user registration, task creation, and category management.

## Tech Stack

- **Backend**: Flask 2.3.3, Python
- **Database**: MySQL (development) / PostgreSQL (production)
- **Authentication**: Flask-Login with Werkzeug password hashing
- **Frontend**: HTML5, CSS3, Bootstrap 5, Jinja2
- **Deployment**: Render.com with Gunicorn WSGI server
- **Environment**: python-dotenv for configuration management

## Quick Start

### Prerequisites
- Python 3.8+
- MySQL (for local development)
- Git

### Local Installation

1. **Clone the repository**
```bash
git clone https://github.com/nihal-kabir/HaatKhata.git
cd HaatKhata
```

2. **Set up virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

5. **Initialize database**
```bash
python init_db.py
```

6. **Run the application**
```bash
python app.py
```

Visit `http://localhost:5000` to access the application.

## Database Schema

| Table | Purpose | Key Features |
|-------|---------|-------------|
| **user** | User management | Secure authentication, profile data |
| **category** | Task organization | Custom colors, descriptions |
| **task** | Task storage | Priority levels, due dates, status tracking |

## Deployment

The application is production-ready with:
- Environment-based configuration
- Database connection retry logic
- Proper error handling and logging
- Scalable architecture for cloud deployment

### Deploy to Render
1. Fork this repository
2. Create a new Web Service on [Render](https://render.com)
3. Connect your repository
4. Add PostgreSQL database
5. Configure environment variables
6. Deploy automatically

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Author

**Nihal Kabir**
- GitHub: [@nihal-kabir](https://github.com/nihal-kabir)
- Live Demo: [HaatKhata](https://haatkhata-37ry.onrender.com)

---

<div align="center">
  <strong>Built with ❤️ using Flask and Bootstrap</strong>
</div>
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