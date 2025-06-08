# src/logger.py
import time
import logging

logging.basicConfig(filename="app.log", level=logging.INFO)

def log_timing(label):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            elapsed = round(end - start, 2)
            logging.info(f"{label}: {elapsed} sec")
            return result
        return wrapper
    return decorator

# Test
if __name__ == "__main__":
    @log_timing("SampleFunction")
    def wait():
        time.sleep(1)
    wait()
