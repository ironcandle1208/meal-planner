"""
Logger for the meal planner application.
"""

import logging
import os
import sys
from pathlib import Path


def get_log_dir() -> Path:
    """Get the log directory."""
    home = Path.home()
    if os.name == "nt":  # Windows
        log_dir = home / "AppData" / "Local" / "meals" / "logs"
    elif os.name == "posix":  # macOS/Linux
        if os.uname().sysname == "Darwin":  # macOS
            log_dir = home / "Library" / "Logs" / "meals"
        else:  # Linux
            log_dir = home / ".local" / "share" / "meals" / "logs"
    else:
        log_dir = Path("logs")
    
    # Create the directory if it doesn't exist
    log_dir.mkdir(parents=True, exist_ok=True)
    
    return log_dir


def setup_logger(name: str = "meals") -> logging.Logger:
    """Set up a logger."""
    logger = logging.getLogger(name)
    
    # Set the log level
    logger.setLevel(logging.INFO)
    
    # Create a formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    
    # Create a file handler
    log_file = get_log_dir() / "meals.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    
    # Create a console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


# Create a global logger
logger = setup_logger()