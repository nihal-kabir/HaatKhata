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

- **Backend**: Flask 2.3.3, Python 3.11
- **Database**: PostgreSQL (NeonDB / Render PostgreSQL)
- **ORM**: Raw SQL with psycopg2 (optimized queries)
- **Authentication**: Flask-Login with Werkzeug password hashing
- **Frontend**: HTML5, CSS3, Bootstrap 5, Jinja2
- **Deployment**: Render.com with Gunicorn WSGI server
- **Environment**: python-dotenv for configuration management

## Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 14+ (for local development)
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

4. **Set up PostgreSQL database**
```bash
# Create database
sudo -u postgres createdb task_manager_db

# Or use the provided SQL script
sudo -u postgres psql -f setup_postgres.sql
```

5. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your PostgreSQL credentials
```

6. **Initialize database**
```bash
python init_db.py
```

7. **Run the application**
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

The application is production-ready and optimized for cloud deployment with:
- ✅ Environment-based configuration (DATABASE_URL support)
- ✅ Database connection retry logic with SSL support
- ✅ Health check endpoint for monitoring
- ✅ Gunicorn production server with optimized workers
- ✅ Automatic database initialization on deployment
- ✅ Support for both Render PostgreSQL and NeonDB

### Quick Deploy to Render + NeonDB

#### Option 1: One-Click Deploy with Render Blueprint
1. Click the button below to deploy:

   [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

2. Connect your GitHub repository
3. Set up NeonDB (recommended) or use Render PostgreSQL
4. Configure environment variables
5. Deploy! 🚀

#### Option 2: Manual Setup (NeonDB)
1. **Set up NeonDB**:
   - Create account at [neon.tech](https://neon.tech)
   - Create new project
   - Copy the connection string

2. **Deploy to Render**:
   - Create new Web Service at [render.com](https://render.com)
   - Connect your repository
   - Set build command: `./build.sh`
   - Set start command: `gunicorn -c gunicorn_config.py app:app`
   - Add environment variable: `DATABASE_URL` (NeonDB connection string)
   - Add environment variable: `SECRET_KEY` (use generator)
   - Deploy!

📖 **[Complete Deployment Guide](DEPLOYMENT.md)** - Detailed step-by-step instructions

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<div align="center">
  <strong>CSE370: Database Systems</strong>
</div>
