#!/usr/bin/env python3
"""
Database initialization script for HaatKhata
Run this script to create database tables and insert default data.
"""

from database import DatabaseManager

def main():
    """Initialize database tables and default data"""
    try:
        db_manager = DatabaseManager()
        print("Initializing database...")
        
        db_manager.init_database()
        print("Database initialized successfully!")
        
    except Exception as e:
        print(f"Database initialization failed: {e}")
        raise

if __name__ == "__main__":
    main()