"""
Database connection and session management.
"""

import os
from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from meals.models import Base
from meals.utils.exceptions import DatabaseException

# Get the app data directory
def get_app_data_dir() -> Path:
    """Get the application data directory."""
    home = Path.home()
    if os.name == "nt":  # Windows
        app_data = home / "AppData" / "Local" / "meals"
    elif os.name == "posix":  # macOS/Linux
        if os.uname().sysname == "Darwin":  # macOS
            app_data = home / "Library" / "Application Support" / "meals"
        else:  # Linux
            app_data = home / ".local" / "share" / "meals"
    else:
        raise DatabaseException(f"Unsupported operating system: {os.name}")
    
    # Create the directory if it doesn't exist
    app_data.mkdir(parents=True, exist_ok=True)
    
    return app_data

# Database file path
DB_PATH = get_app_data_dir() / "meals.db"

# Create SQLite engine
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables() -> None:
    """Create all tables in the database."""
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        raise DatabaseException(f"Failed to create database tables: {str(e)}")


def get_db_session() -> Generator[Session, None, None]:
    """Get a database session."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def init_db() -> None:
    """Initialize the database."""
    try:
        create_tables()
    except Exception as e:
        raise DatabaseException(f"Failed to initialize database: {str(e)}")