# Use the official Python image from the Docker Hub
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port your app runs on (optional, as Railway automatically manages ports)
EXPOSE 5000

# Command to run your application with proper environment variable substitution
CMD ["sh", "-c", "gunicorn -w 4 -b 0.0.0.0:$PORT server:app"]
