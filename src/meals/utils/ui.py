"""
UI utilities for the meal planner application.
"""

import asyncio
import functools
import threading
from typing import Any, Callable, Optional, TypeVar

import toga
from toga.style import Pack

from meals.utils.logger import logger

T = TypeVar("T")


def run_in_background(func: Callable) -> Callable:
    """
    Run a function in a background thread.
    
    Args:
        func: Function to run in the background.
    
    Returns:
        Decorated function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> None:
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
    
    return wrapper


def run_async(func: Callable) -> Callable:
    """
    Run a function asynchronously.
    
    Args:
        func: Function to run asynchronously.
    
    Returns:
        Decorated function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> asyncio.Future:
        return asyncio.ensure_future(func(*args, **kwargs))
    
    return wrapper


def debounce(wait_time: float) -> Callable:
    """
    Debounce a function call.
    
    Args:
        wait_time: Time to wait in seconds.
    
    Returns:
        Decorated function.
    """
    def decorator(func: Callable) -> Callable:
        timer: Optional[threading.Timer] = None
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> None:
            nonlocal timer
            if timer is not None:
                timer.cancel()
            timer = threading.Timer(wait_time, func, args=args, kwargs=kwargs)
            timer.start()
        
        return wrapper
    
    return decorator


def create_loading_indicator() -> toga.Box:
    """
    Create a loading indicator.
    
    Returns:
        Loading indicator box.
    """
    box = toga.Box(style=Pack(direction="column", alignment="center", padding=20))
    label = toga.Label("読み込み中...", style=Pack(text_align="center", padding=10))
    activity_indicator = toga.ActivityIndicator(style=Pack(padding=10))
    activity_indicator.start()
    box.add(activity_indicator)
    box.add(label)
    return box


def show_loading(window: toga.Window, message: str = "読み込み中...") -> toga.Box:
    """
    Show a loading indicator in a window.
    
    Args:
        window: Window to show the loading indicator in.
        message: Message to display.
    
    Returns:
        Loading indicator box.
    """
    # Create a semi-transparent overlay
    overlay = toga.Box(style=Pack(
        direction="column",
        alignment="center",
        flex=1,
        background_color=(0, 0, 0, 0.5),
    ))
    
    # Create a loading box
    loading_box = toga.Box(style=Pack(
        direction="column",
        alignment="center",
        padding=20,
        background_color=(1, 1, 1, 1),
        border_color=(0, 0, 0, 0.2),
        border_width=1,
    ))
    
    # Add loading indicator and message
    activity_indicator = toga.ActivityIndicator(style=Pack(padding=10))
    activity_indicator.start()
    label = toga.Label(message, style=Pack(text_align="center", padding=10))
    
    loading_box.add(activity_indicator)
    loading_box.add(label)
    overlay.add(loading_box)
    
    # Save the original content
    original_content = window.content
    
    # Show the loading overlay
    window.content = overlay
    
    return original_content


def hide_loading(window: toga.Window, original_content: toga.Box) -> None:
    """
    Hide the loading indicator and restore the original content.
    
    Args:
        window: Window to hide the loading indicator from.
        original_content: Original content to restore.
    """
    window.content = original_content