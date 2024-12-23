from datetime import datetime
from functools import wraps

def log_execution_time(func):
    """A decorator to log the execution time of a function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        result = func(*args, **kwargs)
        end_time = datetime.now()
        print(f"Execution time: {end_time - start_time}")
        return result
    return wrapper

def handle_exceptions(func):
    """A decorator to handle exceptions."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as e:
            print(f"Error: File not found - {e}")
        except Exception as e:
            print(f"Error occurred in '{func.__name__}': {e}")
    return wrapper