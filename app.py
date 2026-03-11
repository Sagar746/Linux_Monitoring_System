from flask import Flask, render_template
from pyfiglet import Figlet
import os

import psutil
import webbrowser
import threading

import pyttsx3
import threading
import time

from datetime import datetime
from tqdm import tqdm


app = Flask(__name__)



# first startup screen when running code.
def startup_screen():
    f = Figlet(font="slant")
    print(f.renderText("System Monitor"))

    print("Starting System Monitor...\n")

    for i in tqdm(range(100)):
        time.sleep(0.02)

    print("\n Dashboard Ready")
    print(" Opening browser...\n")

print("Dashboard running at http://localhost:8000")


# This will open a browser using webbrowser
def open_browser():
    webbrowser.open("http://127.0.0.1:8000")
    


def clear_terminal():
    os.system('clear' if os.name == 'posix' else 'cls')



# ANSI escape codes for colored terminal text
RED = "\033[91m"
RESET = "\033[0m"


def trigger_voice_alert(resource_name, value):
    """Speaks a warning using a female system voice."""
    
    def speak():
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        # Logic to find a female voice (usually index 1 on Windows, or search by name)
        female_voice = None
        for voice in voices:
            if "female" in voice.name.lower() or "zira" in voice.name.lower() or "samantha" in voice.name.lower():
                female_voice = voice.id
                break
        
        if female_voice:
            engine.setProperty('voice', female_voice)
        
        # Settings for a "sweet" tone: slower and slightly higher pitch
        engine.setProperty('rate', 145)  # Slightly slower than default (200)
        engine.setProperty('volume', 0.9) 

        message = f"{resource_name} usage is a bit high, it is at {value} percent."
        engine.say(message)
        engine.runAndWait()

    # Run in a separate thread so the dashboard doesn't lag while she speaks
    threading.Thread(target=speak, daemon=True).start()



# Store the last time an alert was spoken
last_alert_time = {"CPU": 0, "Memory": 0, "disk":0}

def check_thresholds(stats):
    current_time = time.time()
    cooldown_seconds = 10 

    # Check CPU
    if stats['cpu'] >= 50:
        if current_time - last_alert_time["CPU"] > cooldown_seconds:
            trigger_voice_alert("C P U", stats['cpu'])
            last_alert_time["CPU"] = current_time

    # Check Memory
    if stats['memory'] >= 85:
        if current_time - last_alert_time["Memory"] > cooldown_seconds:
            trigger_voice_alert("Memory", stats['memory'])
            last_alert_time["Memory"] = current_time


    # Check Disk
    if stats['disk'] >= 6.5:
        if current_time - last_alert_time["disk"] > cooldown_seconds:
            trigger_voice_alert("Disk", stats['disk'])
            last_alert_time["disk"] = current_time



# Function to get system stats
def get_system_stats():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    memory_usage = memory.percent
    disk = psutil.disk_usage('/')
    disk_usage = disk.percent

    stats= {
        "cpu": cpu_usage,
        "memory": memory_usage,
        "disk": disk_usage,
    }
    check_thresholds(stats)
    log_stats(stats)
    return stats

# Function to log stats to a file
def log_stats(stats):
    with open("system_monitor.log", "a") as log_file:
        log_file.write(f"{datetime.now()}: CPU: {stats['cpu']}%, Memory: {stats['memory']}%, Disk: {stats['disk']}%\n")

# Main function
def main():
    print("Linux System Monitor")
    print("Press Ctrl+C to exit.")

    try:
        while True:
            clear_terminal()
            stats = get_system_stats()

            print(f"Time: {["datetime.now().strftime('%Y-%m-%d %H:%M:%S')"]}")
            print(f"CPU Usage: {stats['cpu']}%")
            print(f"Memory Usage: {stats['memory']}%")
            print(f"Disk Usage: {stats['disk']}%")

            log_stats(stats)
            time.sleep(10)  # Update every 5 seconds
    except KeyboardInterrupt:
        print("\nExiting System Monitor.")



@app.route("/")
def dashboard():
    stats = get_system_stats()
    
    # Create a list of active alerts to show on the webpage
    active_alerts = []
    if stats['cpu'] >= 50:
        active_alerts.append(f"CPU usage is high: {stats['cpu']}%")
    if stats['memory'] >= 85:
        active_alerts.append(f"Memory usage is high: {stats['memory']}%")

    if stats['disk'] >= 6.5:
        active_alerts.append(f"Disk usage is high: {stats['disk']}%")
        
    return render_template(
        "index.html", 
        stats=stats, 
        alerts=active_alerts, 
        datetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )


print(f'Unix Like operating system: {os.name}')

if __name__ == "__main__":
    startup_screen()
    
    threading.Timer(1, open_browser).start()

    app.run(debug=True,port=8000, use_reloader=False)






