
# HaatKhata

> **কাজ শেষ, খাতা ফাঁকা** - A modern task management web application built with Flask

[![Live Demo](https://img.shields.io/badge/Live%20Demo--brightgreen?style=for-the-badge)](https://haatkhata.onrender.com/)

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

**[View Live Application →](https://haatkhata.onrender.com/)**

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
````

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

| Table        | Purpose           | Key Features                                |
| ------------ | ----------------- | ------------------------------------------- |
| **user**     | User management   | Secure authentication, profile data         |
| **category** | Task organization | Custom colors, descriptions                 |
| **task**     | Task storage      | Priority levels, due dates, status tracking |

## Deployment

The application is production-ready with:

* Environment-based configuration
* Database connection retry logic
* Proper error handling and logging
* Scalable architecture for cloud deployment

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

<div align="center">
  <strong>CSE370: Database Systems</strong>
</div>
```
