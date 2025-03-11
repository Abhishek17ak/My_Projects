from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from functools import wraps
import datetime
import time
from marshmallow import Schema, fields as ma_fields, validate, ValidationError
from prometheus_client import Counter, Histogram, start_http_server
import threading

from .config import config
from .utils.logging import logger
from .models.summarizer import get_summarizer, SummarizerException
from .models.database import init_db, get_session, store_summary, TextChunk

# Initialize Flask app
app = Flask(__name__)

# Initialize API with Swagger documentation
api = Api(
    app, 
    version='1.0', 
    title='Financial Report Summarizer API',
    description='API for summarizing financial reports',
    doc='/docs'
)

# Define namespaces
ns = api.namespace('summarizer', description='Summarization operations')
health_ns = api.namespace('health', description='Health check operations')

# Initialize database
init_db()

# API keys for authentication
API_KEYS = {
    "your_api_key_1": {"user": "user1", "rate_limit": 100},
    "your_api_key_2": {"user": "user2", "rate_limit": 50}
}

# Rate limiting
rate_limits = {}

# Prometheus metrics
SUMMARY_REQUESTS = Counter('summary_requests_total', 'Total number of summary requests')
SUMMARY_ERRORS = Counter('summary_errors_total', 'Total number of summary errors')
SUMMARY_PROCESSING_TIME = Histogram('summary_processing_seconds', 'Time spent processing summaries')

# Start metrics server in a separate thread
def start_metrics_server():
    start_http_server(8000)

threading.Thread(target=start_metrics_server, daemon=True).start()

# Authentication decorator
def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        
        if not api_key or api_key not in API_KEYS:
            logger.warning(f"Unauthorized API access attempt from {request.remote_addr}")
            return {"error": "Unauthorized"}, 401
        
        # Rate limiting
        user_info = API_KEYS[api_key]
        current_time = time.time()
        
        if api_key not in rate_limits:
            rate_limits[api_key] = {"count": 0, "reset_time": current_time + 3600}
        
        if current_time > rate_limits[api_key]["reset_time"]:
            rate_limits[api_key] = {"count": 0, "reset_time": current_time + 3600}
        
        if rate_limits[api_key]["count"] >= user_info["rate_limit"]:
            logger.warning(f"Rate limit exceeded for {user_info['user']}")
            return {"error": "Rate limit exceeded"}, 429
        
        rate_limits[api_key]["count"] += 1
        
        # Log access
        logger.info(f"API access by {user_info['user']}")
        return f(*args, **kwargs)
    
    return decorated

# Input validation schemas
class SummarizeRequestSchema(Schema):
    text = ma_fields.String(required=True, validate=validate.Length(min=100, max=50000))
    max_length = ma_fields.Integer(missing=config["model"]["max_length"], validate=validate.Range(min=50, max=500))
    min_length = ma_fields.Integer(missing=config["model"]["min_length"], validate=validate.Range(min=20, max=100))

# API models for documentation
summarize_model = api.model('SummarizeRequest', {
    'text': fields.String(required=True, description='Text to summarize'),
    'max_length': fields.Integer(default=config["model"]["max_length"], description='Maximum summary length'),
    'min_length': fields.Integer(default=config["model"]["min_length"], description='Minimum summary length')
})

summary_response = api.model('SummaryResponse', {
    'summary': fields.String(description='Generated summary'),
    'original_length': fields.Integer(description='Length of original text'),
    'summary_length': fields.Integer(description='Length of summary'),
    'processing_time': fields.Float(description='Processing time in seconds')
})

# API endpoints
@ns.route('/summarize')
class Summarize(Resource):
    @api.doc('summarize_text', security='apikey')
    @api.expect(summarize_model)
    @api.marshal_with(summary_response)
    @require_api_key
    def post(self):
        """Generate a summary from financial text"""
        SUMMARY_REQUESTS.inc()
        start_time = time.time()
        
        try:
            # Validate input
            schema = SummarizeRequestSchema()
            try:
                data = schema.load(request.json)
            except ValidationError as err:
                logger.warning(f"Validation error: {err.messages}")
                SUMMARY_ERRORS.inc()
                return {"error": err.messages}, 400
            
            text = data['text']
            max_length = data['max_length']
            min_length = data['min_length']
            
            # Generate summary
            summarizer = get_summarizer()
            
            with SUMMARY_PROCESSING_TIME.time():
                summary = summarizer.generate_summary_for_long_text(
                    text, 
                    max_length=max_length, 
                    min_length=min_length
                )
            
            processing_time = time.time() - start_time
            
            # Store in database (async in production)
            try:
                session = get_session()
                # Create a dummy chunk for storage
                # In a real app, this would link to actual chunks
                chunk = TextChunk(
                    section_id=1,  # Placeholder
                    chunk_index=0,
                    content=text[:1000] + "..." if len(text) > 1000 else text
                )
                session.add(chunk)
                session.commit()
                
                # Store the summary
                store_summary(
                    chunk.id,
                    summary,
                    max_length,
                    min_length,
                    summarizer.model_name
                )
            except Exception as e:
                logger.error(f"Error storing summary in database: {str(e)}")
                # Don't fail the request if storage fails
            
            return {
                'summary': summary,
                'original_length': len(text),
                'summary_length': len(summary),
                'processing_time': processing_time
            }
            
        except SummarizerException as e:
            SUMMARY_ERRORS.inc()
            logger.error(f"Summarizer error: {str(e)}")
            return {"error": str(e)}, 500
            
        except Exception as e:
            SUMMARY_ERRORS.inc()
            logger.error(f"Unexpected error: {str(e)}")
            return {"error": "An unexpected error occurred"}, 500

@health_ns.route('')
class HealthCheck(Resource):
    def get(self):
        """Check system health"""
        # Check database connection
        try:
            session = get_session()
            session.execute('SELECT 1')
            session.close()
            db_status = "healthy"
        except Exception as e:
            db_status = f"unhealthy: {str(e)}"
        
        # Check model loading
        try:
            summarizer = get_summarizer()
            model_status = "healthy"
        except Exception as e:
            model_status = f"unhealthy: {str(e)}"
        
        status = {
            "status": "healthy" if db_status == "healthy" and model_status == "healthy" else "unhealthy",
            "database": db_status,
            "model": model_status,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
        
        return status, 200 if status["status"] == "healthy" else 500

if __name__ == '__main__':
    # Run the Flask app
    app.run(
        host=config["api"]["host"],
        port=config["api"]["port"],
        debug=config["api"]["debug"]
    ) 