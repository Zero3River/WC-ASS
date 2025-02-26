FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=jwt_service.py \
    FLASK_ENV=production

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY JWT_service.py .

# Expose the port the app runs on
EXPOSE 8002

# Run the application
# CMD ["gunicorn", "--bind", "0.0.0.0:8002", "JWT_service:app"]
CMD ["python", "JWT_service.py"]