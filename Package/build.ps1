Set-Location ..
# Ensure that the script stops on the first error
$ErrorActionPreference = "Stop"

# Define the Python script name
$scriptName = "Serv.py"
$exeName = "Serv.exe"
$finalExeName = "sdb.exe"
$iconUrl = "https://files.catbox.moe/405st1.ico"
$expatch = (Get-Item .).FullName
Clear-Host
Write-Output "Installing necessary packages..."

pip install pyinstaller --quiet
pip install pipreqs --quiet

Clear-Host

Write-Output "Generating requirements.txt file..."
pipreqs ./ --encoding=utf8

Clear-Host

Write-Output "Downloading App packages..."
pip install -r requirements.txt --quiet

Clear-Host

Write-Output "Downloading App Icon..."
Invoke-WebRequest $iconUrl -OutFile icon.ico

Clear-Host

Write-Output "Building..."
# Package the Python script using pyinstaller
pyinstaller -F -i="$expatch/icon.ico" $scriptName
# Delete the sdb file in the current directory if it exists
if (Test-Path "./sdb.exe") {
    Remove-Item -Path "./sdb.exe" -Force
}

# Delete the Serv.spec file if it exists
if (Test-Path "./Serv.spec") {
    Remove-Item -Path "./Serv.spec" -Force
}

# Delete the build folder if it exists
if (Test-Path "./build") {
    Remove-Item -Path "./build" -Recurse -Force
}
if (Test-Path "./package.bat") {
    Remove-Item -Path "./package.bat" -Recurse -Force
}
if (Test-Path "./icon.ico") {
    Remove-Item -Path "./icon.ico" -Recurse -Force
}

# Copy the executable from the dist folder and rename it to sdb.exe
if (Test-Path "./dist/$exeName") {
    Copy-Item -Path "./dist/$exeName" -Destination "./$finalExeName" -Force
} else {
    Write-Error "Executable not found in dist folder."
}

# Clean up the dist folder if needed
Remove-Item -Path "./dist" -Recurse -Force
Remove-Item $PSCommandPath -Force
exit
