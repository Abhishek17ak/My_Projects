FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV API_URL=http://api:5000
ENV API_KEY=your_api_key_1

EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "web/app.py", "--server.port=8501", "--server.address=0.0.0.0"] 