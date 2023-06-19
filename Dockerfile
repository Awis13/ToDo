FROM python:3.9

# Your existing Dockerfile instructions

# Copy frontend files
COPY frontend /app/frontend

# Set the working directory
WORKDIR /app

# Install dependencies
RUN pip install -r frontend/requirements.txt

# Expose the desired port
EXPOSE 5000

# Start the application
CMD ["python", "app.py"]
