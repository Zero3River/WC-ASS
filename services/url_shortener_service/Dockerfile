# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /url_shortener_service

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Expose the port 8000 for Flask to run on
EXPOSE 8000

# Command to run on container start
CMD ["python", "RESTful_API.py"]
