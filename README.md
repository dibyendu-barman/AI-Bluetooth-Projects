## File & Folder Commands ##

# Create folder
New-Item -ItemType Directory MyFolder

# Create file
New-Item -ItemType File notes.txt

# Read file
Get-Content notes.txt

# Write text to file
"Hello PowerShell" | Out-File notes.txt

# Add text to file
"New line" | Add-Content notes.txt

# Copy file
Copy-Item notes.txt backup.txt

# Move file
Move-Item notes.txt .\MyFolder\

# Rename file
Rename-Item notes.txt new_notes.txt

# Delete file
Remove-Item new_notes.txt

# Delete folder
Remove-Item MyFolder -Recurse

## Python / Project Commands ##

# Check Python version
python --version

# Check pip
pip --version

# Create virtual environment
python -m venv venv

# Activate venv
.\venv\Scripts\Activate.ps1

# Deactivate venv
deactivate

# Install package
pip install requests

# Show installed packages
pip list

# Save packages
pip freeze > requirements.txt

# Install requirements
pip install -r requirements.txt

# Run Python file
python app.py

## Network / System ##

# IP information
ipconfig

# Detailed network information
Get-NetIPConfiguration

# Test connection
Test-Connection google.com

# Check running processes
Get-Process

# Stop process
Stop-Process -Name notepad

# Check services
Get-Service

# Check environment variables
Get-ChildItem Env:

## Very Useful Shortcuts ##

Tab          # Auto-complete
↑ / ↓        # Command history
Ctrl + C     # Stop running command
Ctrl + L     # Clear screen
