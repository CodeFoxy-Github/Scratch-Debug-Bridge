#!/bin/bash

cd ..

# Define the Python script name and other variables
script_name="Serv.py"
final_file_name="sdb"
icon_url="https://files.catbox.moe/405st1.ico"
build_name="Serv"
# Get the full path of the current directory
expath=$(pwd)

# clear the terminal
clear

# Install necessary packages
echo "Installing necessary packages..."
pip install pyinstaller
pip install pipreqs

# clear the terminal
clear

# Generate requirements.txt file
echo "Generating requirements.txt file..."
pipreqs ./ --encoding=utf8

# clear the terminal
clear

# Download App packages
echo "Downloading App packages..."
pip install -r requirements.txt

# clear the terminal
clear

# Download App Icon
echo "Downloading App Icon..."
wget -O icon.ico $icon_url

# clear the terminal
clear

# Build the executable
echo "Building..."
pyinstaller -F --icon="$expath/icon.ico" $script_name
# lemme test

echo "Build complete."
exit 0
