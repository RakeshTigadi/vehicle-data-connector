# Use official Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements first and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Set environment variable to avoid buffering
ENV PYTHONUNBUFFERED=1

# Run the app using uvicorn with the expected port
CMD ["python", "main.py"]
