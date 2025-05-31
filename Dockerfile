FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY api/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY api/ .

# Create data directory
RUN mkdir -p data

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "app.py"] 