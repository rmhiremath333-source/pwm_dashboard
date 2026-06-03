import csv
import os
from datetime import datetime

LOG_FILE = "logs/pwm_log.csv"

def init():
    os.makedirs("logs", exist_ok=True)
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "duty_%", "freq_hz", "power_mw", "saved_mw", "period_ms", "on_ms", "off_ms", "band"])
        print("[Logger] Log file created at logs/pwm_log.csv")

def log(duty, freq, data):
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            duty,
            freq,
            data["power_mw"],
            data["saved_mw"],
            data["period_ms"],
            data["on_ms"],
            data["off_ms"],
            data["band"]
        ])
    print(f"[Logger] duty={duty}%  freq={freq}Hz  power={data['power_mw']}mW  saved={data['saved_mw']}mW")

def read_all():
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r") as f:
        reader = csv.DictReader(f)
        return list(reader)

def clear():
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    init()
    print("[Logger] Log cleared.")