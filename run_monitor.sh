#!/bin/bash

# Define app name
APP_NAME="Monitor System"

echo "------------------------------------------"
echo "  Setting up $APP_NAME Environment...  "
echo "------------------------------------------"

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Error: Python3 is not installed."
    exit
fi

# Create templates directory if it doesn't exist
if [ ! -d "templates" ]; then
    mkdir templates
    echo "📁 Created 'templates' folder."
fi

#create a virtual environemnt
if [ ! -d "env" ]; then
    echo "🛠️ Creating Virtual Environment..."
    python3 -m venv env
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip3 install flask pyfiglet psutil tqdm pyttsx3 --quiet

# Run the Python script
echo "Launching Application..."
python3 app.py