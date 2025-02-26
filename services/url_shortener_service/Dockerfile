# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the app files
COPY . .

# Expose port 8000 for Flask
EXPOSE 8000

# Command to run on container start
CMD ["python", "RESTful_API.py"]
