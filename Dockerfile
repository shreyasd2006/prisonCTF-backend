# Use an official, lightweight Python image as the base.
# This specifies the exact version of Python to use.
FROM python:3.12-slim

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the requirements file first. This is a Docker optimization.
COPY requirements.txt .

# Install all the Python libraries your application needs.
RUN pip install --no-cache-dir -r requirements.txt

# Now, copy the rest of your application's code into the container.
COPY . .

# Tell Docker that the application will listen on port 8000.
# Azure will automatically connect its public port 80 to this.
EXPOSE 8000

# The command that will be run to start your application.
# This replaces the "Startup Command" field in the Azure Portal.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend_server:app"]