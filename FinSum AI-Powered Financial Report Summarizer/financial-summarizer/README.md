# Finsum AI-Powered Financial Report Summarizer

A powerful tool that automatically extracts and condenses key information from financial reports and documents.

![Financial Report Summarizer](https://img.shields.io/badge/Financial-Summarizer-blue)
![Python](https://img.shields.io/badge/Python-3.9+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📊 Overview

The Financial Report Summarizer is a comprehensive system designed to help financial professionals, analysts, and investors quickly extract key insights from lengthy financial documents. Using advanced natural language processing techniques, the system identifies and prioritizes the most significant financial data points, metrics, and business highlights.

### Key Features

- **Automatic Summarization**: Extract the most important information from financial reports
- **Web Interface**: User-friendly Streamlit interface for easy interaction
- **API Access**: RESTful API for integration with other systems
- **Database Integration**: Store and retrieve processed documents
- **Authentication**: Secure API access with API key authentication
- **Docker Support**: Easy deployment with Docker and docker-compose

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Docker and docker-compose (optional, for containerized deployment)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/financial-summarizer.git
   cd financial-summarizer
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

#### Option 1: Using Python directly

1. Start the API server:
   ```bash
   # Windows PowerShell
   $env:FLASK_APP = "app/api.py"
   $env:CONFIG_FILE = "config.yaml"
   python -m flask run --host=0.0.0.0 --port=5000
   
   # Linux/Mac
   export FLASK_APP=app/api.py
   export CONFIG_FILE=config.yaml
   python -m flask run --host=0.0.0.0 --port=5000
   ```

2. Start the web interface (in a separate terminal):
   ```bash
   python -m streamlit run web/app.py
   ```

#### Option 2: Using the simplified summarizer

If you encounter issues with the API server, you can use the simplified summarizer:

```bash
python -m streamlit run simple_summarizer.py
```

#### Option 3: Using Docker (recommended for production)

```bash
docker-compose up -d
```

### Accessing the Application

- Web Interface: http://localhost:8501
- API: http://localhost:5000
- API Documentation: http://localhost:5000/api/doc

## 🔧 Architecture

The system consists of two main components:

1. **API Service (Flask)**
   - RESTful API for summarization
   - Authentication and validation
   - Database integration
   - Error handling and logging

2. **Web Interface (Streamlit)**
   - User-friendly interface
   - Text input and file upload
   - Visualization of results
   - Integration with API

## 📝 API Documentation

### Endpoints

- `POST /summarizer/summarize`: Generate a summary from text
  ```json
  {
    "text": "Your financial text here...",
    "max_length": 200,
    "min_length": 50
  }
  ```

- `GET /health`: Check system health
- `GET /metrics`: Prometheus metrics

### Authentication

All API requests require an API key in the `X-API-Key` header.

## 🧪 Testing

Run the test suite:

```bash
python -m pytest
```

## 🔒 Security

- API key authentication
- Input validation
- Error handling
- Secure database operations

## 📈 Future Improvements

- PDF and DOCX file support
- SEC EDGAR integration
- Advanced summarization models
- User management system
- Summary comparison tools

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request 