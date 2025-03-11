FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV FLASK_APP=app/api.py
ENV FLASK_ENV=production
ENV MODEL_PATH=/app/models/cache

# Create necessary directories
RUN mkdir -p /app/models/cache /app/logs

# Download NLTK data
RUN python -c "import nltk; nltk.download('punkt')"

# Remove the model download step from build time
# The model will be downloaded at runtime when first needed

EXPOSE 5000
EXPOSE 8000

# Run with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "app.api:app"] 