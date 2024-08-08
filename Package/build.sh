#!/bin/bash

cd ..

# Define the Python script name and other variables
script_name="Serv.py"
final_file_name="sdb-amd64-linux"
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

# Delete the Serv.spec file if it exists
if [ -f "./Serv.spec" ]; then
    rm "./Serv.spec"
fi
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
if [ -f "./dist/$build_name" ]; then
    cp "./dist/$build_name" "./Build/$final_file_name"
else
    echo "Executable not found in dist folder."
    exit 1
fi
cd Build
ls
# Clean up the dist folder
rm -rf "./dist"

echo "Build complete."
exit 0
