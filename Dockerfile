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

# Run the app with Gunicorn, limit workers to 1 to avoid memory issues
CMD ["sh", "-c", "gunicorn -w 1 -b 0.0.0.0:${PORT:-5000} server:app"]
