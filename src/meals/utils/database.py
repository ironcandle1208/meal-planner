"""
Database connection and session management.
"""

import os
import sqlite3
import time
from pathlib import Path
from typing import Generator, Optional

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from meals.models import Base
from meals.utils.exceptions import DatabaseException
from meals.utils.logger import logger

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

# Enable foreign keys for SQLite
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Enable foreign keys for SQLite."""
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

# Create SQLite engine with connection pooling and optimized settings
engine = create_engine(
    f"sqlite:///{DB_PATH}",
    connect_args={
        "check_same_thread": False,
        "timeout": 30,  # Connection timeout in seconds
    },
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=10,
    max_overflow=20,
    echo=False,  # Set to True for SQL query logging
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create scoped session for thread safety
ScopedSession = scoped_session(SessionLocal)


def create_tables() -> None:
    """Create all tables in the database."""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except SQLAlchemyError as e:
        logger.error(f"Failed to create database tables: {str(e)}")
        raise DatabaseException(f"Failed to create database tables: {str(e)}")


def get_db_session() -> Generator[Session, None, None]:
    """Get a database session."""
    session = ScopedSession()
    try:
        yield session
    except Exception as e:
        logger.error(f"Error in database session: {str(e)}")
        session.rollback()
        raise
    finally:
        ScopedSession.remove()  # Remove session from registry


def init_db(max_retries: int = 3, retry_delay: int = 1) -> None:
    """Initialize the database with retry logic."""
    retries = 0
    last_error = None
    
    while retries < max_retries:
        try:
            create_tables()
            return
        except OperationalError as e:
            last_error = e
            retries += 1
            logger.warning(f"Database initialization failed (attempt {retries}/{max_retries}): {str(e)}")
            time.sleep(retry_delay)
    
    # If we get here, all retries failed
    logger.error(f"Failed to initialize database after {max_retries} attempts")
    raise DatabaseException(f"Failed to initialize database after {max_retries} attempts: {str(last_error)}")


def backup_database() -> Optional[Path]:
    """Backup the database."""
    try:
        import shutil
        from datetime import datetime
        
        # Create backup directory
        backup_dir = get_app_data_dir() / "backups"
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Create backup file name with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_dir / f"meals_{timestamp}.db"
        
        # Copy the database file
        shutil.copy2(DB_PATH, backup_path)
        
        logger.info(f"Database backup created at {backup_path}")
        return backup_path
    except Exception as e:
        logger.error(f"Failed to backup database: {str(e)}")
        return None


def restore_database(backup_path: Path) -> bool:
    """Restore the database from a backup."""
    try:
        import shutil
        
        # Check if backup file exists
        if not backup_path.exists():
            raise FileNotFoundError(f"Backup file not found: {backup_path}")
        
        # Close all connections
        engine.dispose()
        
        # Copy the backup file to the database file
        shutil.copy2(backup_path, DB_PATH)
        
        logger.info(f"Database restored from {backup_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to restore database: {str(e)}")
        return False