#!/bin/bash

# Switch to Docker settings
echo "Switching to Docker settings..."

# Check if backup file exists
if [ -f "pharmacy_api/settings/development.py.docker.bak" ]; then
    # Restore the Docker settings from backup
    cp pharmacy_api/settings/development.py.docker.bak pharmacy_api/settings/development.py
    rm pharmacy_api/settings/development.py.docker.bak
    echo "Successfully switched to Docker settings."
else
    # Update the development.py file to use 'db' instead of localhost for PostgreSQL
    sed -i "s/'HOST': 'localhost'/'HOST': 'db'/g" pharmacy_api/settings/development.py
    echo "Successfully switched to Docker settings."
fi