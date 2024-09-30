# Use the official Python image from Docker Hub
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt first to leverage Docker cache
COPY requirements.txt .

# Install required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port that Gunicorn will use
EXPOSE 8080

# Command to run the app using Gunicorn with Gevent workers
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:${PORT:-8000}", "server:app"]

