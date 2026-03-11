# System Monitoring Dashboard

A real-time **system monitoring dashboard** built with Python and Flask that tracks **CPU usage, memory usage, and disk usage**. The application displays system statistics in a web interface and provides **voice alerts** when system resources exceed defined thresholds.

---

## Features

- Real-time CPU monitoring
- Real-time memory monitoring
- Disk usage monitoring
- Voice alerts when usage exceeds thresholds
- Automatic browser launch
- System statistics logging
- Simple and responsive web dashboard

---

## Technologies Used

- Python
- Flask
- psutil
- pyttsx3
- HTML / CSS
- tqdm
- pyfiglet
- Shell Script

---

## Project Structure
system-monitor
 -app.py
 -system_monitor.log
 -templates/
    -index.html
 - README.md

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Sagar746/Linux_Monitoring_System
cd system-monitor

## Install Required Dependencies
```bash
pip install flask psutil pyttsx3 tqdm pyfiglet
```

## Run run_monitor.sh script
```bash
./run_monitor.sh
```
