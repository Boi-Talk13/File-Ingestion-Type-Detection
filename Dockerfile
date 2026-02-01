# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies needed for python-magic
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements from the parent directory
# Note: Ensure requirements.txt is available to the build context
COPY ../requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files from the Internship directory into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Run the application
# main:app refers to the 'app' object in main.py
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
