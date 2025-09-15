# 🎯 HaatKhata - Smart Task Management System

**হাতেখড়ি থেকে হাতেখাতা - আপনার কাজের খাতা**

## 🌟 What is HaatKhata?

HaatKhata (হাতেখাতা) means "notebook" or "account book" in Bengali, representing the traditional way of keeping track of important tasks and records. This digital version brings the simplicity and effectiveness of a traditional notebook into the modern web era.

## 📋 What We Built

A complete web application with **10 powerful features**:
1. **User Registration & Login** - Secure authentication
2. **Dashboard** - Statistics and overview
3. **Create Tasks** - Add new tasks with details
4. **View All Tasks** - List with filtering and search
5. **Edit Tasks** - Update existing tasks
6. **Delete Tasks** - Remove tasks safely
7. **Task Categories** - Organize tasks by type
8. **Search Tasks** - Find specific tasks quickly
9. **Task Status Tracking** - Mark as pending/in-progress/completed
10. **User Profile** - Manage personal information

## 🛠️ Technology Stack

- **Flask** - Python web framework
- **MySQL** - Database (production-ready)
- **Jinja2** - Template engine (included with Flask)
- **HTML5 & CSS3** - Frontend structure and styling
- **Bootstrap 5** - CSS framework (no custom JavaScript)
- **SQLAlchemy** - Database ORM
- **Docker** - Containerization
- **Gunicorn** - WSGI server
- **Nginx** - Reverse proxy
- **Render.com** - Cloud deployment

## 🗄️ MySQL Database Setup (REQUIRED)

**📖 Read the complete MySQL setup guide: [MYSQL_SETUP.md](MYSQL_SETUP.md)**

### Quick Options:

**Option 1: Docker (Easiest)**
```bash
# Install Docker Desktop, then:
docker-compose up --build
# Go to http://localhost
```

**Option 2: Local MySQL**
```bash
# Install MySQL, create database, then:
cp .env.example .env
# Edit .env with your MySQL credentials
python app.py
```

**⚠️ IMPORTANT: Don't proceed without setting up MySQL first!**

## � Docker Deployment

### Local Development with Docker
```bash
# Start all services (MySQL + Flask + Nginx)
docker-compose up --build

# Your app will be available at:
# http://localhost (Nginx proxy)
# http://localhost:8000 (Direct Flask app)
```

### Production Docker Build
```bash
# Build production image
docker build -t flask-task-manager .

# Run with external MySQL
docker run -e DATABASE_URL=mysql://user:pass@host:3306/db -p 8000:8000 flask-task-manager
```

## 🌐 Deploy to Render.com

### Step 1: Prepare Repository
```bash
# Initialize git repository
git init
git add .
git commit -m "Initial commit"

# Push to GitHub
git remote add origin https://github.com/yourusername/flask-task-manager.git
git push -u origin main
```

### Step 2: Deploy on Render
1. Go to [render.com](https://render.com)
2. Sign up/Login with GitHub
3. Click "New" → "Blueprint"
4. Connect your GitHub repository
5. Render automatically:
   - Creates MySQL database
   - Deploys Flask app with Gunicorn
   - Sets up environment variables
   - Provides HTTPS URL

### Step 3: Environment Variables (Auto-configured)
- `DATABASE_URL` - MySQL connection string
- `SECRET_KEY` - Auto-generated secure key
- `FLASK_ENV` - Set to production

## �📁 Project Structure

```
flask_webapp/
├── app.py                 # Main Flask application
├── models.py              # Database models
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Local development stack
├── nginx.conf            # Nginx reverse proxy config
├── render.yaml           # Render.com deployment config
├── .env.example          # Environment variables template
├── MYSQL_SETUP.md        # Detailed MySQL setup guide
├── templates/            # HTML templates
│   ├── base.html        # Base template with Bootstrap
│   ├── index.html       # Home page
│   ├── login.html       # Login page
│   ├── register.html    # Registration page
│   ├── dashboard.html   # User dashboard
│   ├── tasks.html       # Tasks listing
│   ├── create_task.html # Create task form
│   ├── edit_task.html   # Edit task form
│   ├── categories.html  # Categories management
│   └── profile.html     # User profile
└── static/              # Static files
    └── css/
        └── style.css    # Custom CSS styling
```

## � Quick Start Guide

### For Absolute Beginners:
1. **Setup MySQL** - Follow [MYSQL_SETUP.md](MYSQL_SETUP.md)
2. **Test locally** - Run `python app.py`
3. **Use Docker** - Run `docker-compose up --build`
4. **Deploy** - Push to GitHub → Deploy on Render

### For Docker Users:
```bash
docker-compose up --build
# Visit http://localhost
```

### For Cloud Deployment:
1. Push code to GitHub
2. Connect to Render.com
3. Deploy automatically

## 🎯 Production Features

- **Gunicorn WSGI Server** - Production-ready Python server
- **Nginx Reverse Proxy** - Load balancing and static file serving
- **MySQL Database** - Reliable, scalable database
- **Docker Containers** - Consistent deployment environment
- **Environment Variables** - Secure configuration management
- **HTTPS Ready** - SSL/TLS encryption on Render.com

## 🔒 Security Features

- **Password Hashing** - Werkzeug secure password storage
- **Session Management** - Flask-Login secure sessions
- **CSRF Protection** - Flask-WTF CSRF tokens
- **SQL Injection Prevention** - SQLAlchemy ORM protection
- **Environment Variables** - Sensitive data protection

## 📊 Database Schema

```sql
-- Users table
CREATE TABLE user (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128),
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Categories table
CREATE TABLE category (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    color VARCHAR(7) DEFAULT '#007bff',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tasks table
CREATE TABLE task (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    priority VARCHAR(10) DEFAULT 'medium',
    due_date DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id INT NOT NULL,
    category_id INT,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (category_id) REFERENCES category(id)
);
```

## 🆘 Troubleshooting

### MySQL Connection Issues:
```bash
# Check MySQL status
mysql -u root -p -e "SHOW DATABASES;"

# Reset connection in app
rm task_manager.db  # Remove SQLite if exists
python app.py       # Recreate with MySQL
```

### Docker Issues:
```bash
# Restart everything
docker-compose down -v
docker-compose up --build

# Check logs
docker-compose logs web
docker-compose logs db
```

### Deployment Issues:
- Check Render.com logs
- Verify environment variables
- Ensure GitHub repository is public
- Check render.yaml configuration

## 🎉 Success Checklist

- [ ] MySQL database running
- [ ] Flask app connects to MySQL
- [ ] All 10 features working
- [ ] Docker containers running
- [ ] Deployed to Render.com
- [ ] HTTPS domain working
- [ ] Database persistent after restart

**Your production-ready Flask application is complete!**
