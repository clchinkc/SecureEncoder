import functools
import logging


def log_execution(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Executing {func.__name__} with args={args} kwargs={kwargs}")
        try:
            result = func(*args, **kwargs)
            logging.info(f"Finished {func.__name__} with result={result}")
            return result
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {str(e)}")
            raise e

    return wrapper
