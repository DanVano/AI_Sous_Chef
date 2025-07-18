import datetime
import os

LOG_FILE = os.path.join("logs", "aichef_log.txt")

def log_event(event_type, message):
    os.makedirs("logs", exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{now}] {event_type.upper()}: {message}\n")