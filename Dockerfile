# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Environment variable (optional)
ENV WHEREAMI=DOCKER

# Expose port (for documentation; Cloud Run uses $PORT)
EXPOSE 8080

# Run FastAPI using Uvicorn, listen on Cloud Run PORT
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]