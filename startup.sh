#!/bin/bash

# Exit immediately if any command fails, making it easier to debug.
set -e

# --- STEP 1: INSTALL JAVA DEVELOPMENT KIT (JDK) ---
# This section customizes the standard Python server by adding Java tools.
echo "Updating package lists..."
apt-get update

echo "Installing the Java Development Kit (JDK)..."
# The '-y' flag automatically answers 'yes' to any installation prompts.
apt-get install -y default-jdk

echo "JDK installation complete. Java is now available."
# We'll print the Java version to the logs to confirm it was installed.
java -version

# --- STEP 2: START THE PYTHON WEB SERVER ---
# This is the same Gunicorn command that Azure used to run before.
# Now, it runs only *after* the JDK has been successfully installed.
echo "Starting Gunicorn server..."
gunicorn --bind=0.0.0.0 --timeout 600 backend_server:app