#!/bin/bash

cd ..

# Define the Python script name and other variables
script_name="Serv.py"
final_exe_name="sdb"
icon_url="https://files.catbox.moe/405st1.ico"

# Get the full path of the current directory
expath=$(pwd)

# Clear the terminal
clear

# Install necessary packages
echo "Installing necessary packages..."
pip install pyinstaller
pip install pipreqs

# Clear the terminal
clear

# Generate requirements.txt file
echo "Generating requirements.txt file..."
pipreqs ./ --encoding=utf8

# Clear the terminal
clear

# Download App packages
echo "Downloading App packages..."
pip install -r requirements.txt

# Clear the terminal
clear

# Download App Icon
echo "Downloading App Icon..."
wget -O icon.ico $icon_url

# Clear the terminal
clear

# Build the executable
echo "Building..."
pyinstaller --onefile --icon="$expath/icon.ico" $script_name

# Delete the final executable if it already exists
if [ -f "./$final_exe_name" ]; then
    rm "./$final_exe_name"
fi

# Delete the Serv.spec file if it exists
if [ -f "./Serv.spec" ]; then
    rm "./Serv.spec"
fi

# Delete the build folder if it exists
if [ -d "./build" ]; then
    rm -rf "./build"
fi

# Delete the icon and requirements file if they exist
if [ -f "./icon.ico" ]; then
    rm "./icon.ico"
fi
if [ -f "./requirements.txt" ]; then
    rm "./requirements.txt"
fi

# Copy the executable from the dist folder and rename it to the final name
if [ -f "./dist/$script_name" ]; then
    cp "./dist/$script_name" "./$final_exe_name"
else
    echo "Executable not found in dist folder."
    exit 1
fi

# Clean up the dist folder
rm -rf "./dist"

echo "Build complete."
exit 0
