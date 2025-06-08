# src/utils.py
import datetime

def format_datetime(dt):
    return dt.strftime("%Y-%m-%d %H:%M")

def safe_run(func):
    try:
        return func()
    except Exception as e:
        return f"Error: {e}"

# Test
if __name__ == "__main__":
    print(format_datetime(datetime.datetime.now()))
