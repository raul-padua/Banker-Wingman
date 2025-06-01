# Custom Dockerfile for AWS App Runner
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for better caching)
COPY api/requirements.txt ./api/

# Install Python dependencies
RUN python3 -m pip install --no-cache-dir -r api/requirements.txt

# Copy the entire application
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV OPENAI_API_KEY=your-default-api-key

# Expose port 8000
EXPOSE 8000

# Set the startup command
CMD ["python3", "-m", "uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"] 