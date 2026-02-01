# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies needed for python-magic
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Change working directory to where main.py and static files are located
WORKDIR /app/Internship

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application using uvicorn
# 0.0.0.0 is required for cloud platforms to map the port correctly
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]