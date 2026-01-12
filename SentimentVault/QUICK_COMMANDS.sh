#!/bin/bash
# SentimentVault - Quick Command Reference
# Copy these commands for fast execution

# ============================================================================
# SETUP & INSTALLATION (5 minutes)
# ============================================================================

# Navigate to project
cd /Users/abhishekkalugade/Programming/My_Projects/SentimentVault

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt

# ============================================================================
# REDIS SETUP (2 minutes)
# ============================================================================

# Option 1: Docker (Recommended)
docker run -d -p 6379:6379 --name sentiment-redis redis:7-alpine

# Option 2: Homebrew (macOS)
brew install redis
redis-server

# Verify Redis is running
redis-cli ping
# Expected: PONG

# ============================================================================
# PHASE 1: DATA PREPARATION (10-15 minutes)
# ============================================================================

# Start Jupyter notebook for Phase 1
jupyter notebook notebooks/01_EDA_Data_Preparation.ipynb

# In Jupyter:
# - Go to Cell menu → Run All
# Wait for completion
# Output: data/train_tokenized/, data/test_tokenized/

# ============================================================================
# PHASE 2: MODEL TRAINING (60-240 minutes)
# ============================================================================

# Start Jupyter notebook for Phase 2
jupyter notebook notebooks/02_Model_Training.ipynb

# In Jupyter:
# - Go to Cell menu → Run All
# Wait for training to complete
# Output: models/sentiment_model/, 92%+ F1-Score

# ============================================================================
# PHASE 3: START API SERVER (2 minutes)
# ============================================================================

# Copy environment template
cp .env.example .env

# Start FastAPI server
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# In browser:
# - API Docs: http://localhost:8000/docs
# - API Root: http://localhost:8000

# Test the API
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "This product is amazing!"}'

# ============================================================================
# PHASE 4: LOAD TESTING (5 minutes)
# ============================================================================

# In a NEW terminal window:
cd /Users/abhishekkalugade/Programming/My_Projects/SentimentVault
source venv/bin/activate

# Start load test
locust -f scripts/load_test.py -u 50 -r 5 -t 5m --host http://localhost:8000

# In browser:
# - Locust UI: http://localhost:8089
# Check: 5K+/hour throughput achieved ✅

# ============================================================================
# DOCKER DEPLOYMENT (5 minutes)
# ============================================================================

# Build and start services
docker-compose -f docker/docker-compose.yml up --build -d

# Check services
docker-compose ps

# View logs
docker-compose logs -f api

# Test API
curl http://localhost:8000/health

# Stop services
docker-compose down

# ============================================================================
# GIT & GITHUB PUSH (5 minutes)
# ============================================================================

# Initialize Git
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: SentimentVault v1.0.0 - Production-ready sentiment analysis API"

# Add GitHub remote
git remote add origin https://github.com/YOUR_USERNAME/SentimentVault.git

# Set main branch
git branch -M main

# Push to GitHub
git push -u origin main

# ============================================================================
# DEVELOPMENT COMMANDS
# ============================================================================

# Format code with Black
black backend/ scripts/ notebooks/

# Check code style
flake8 backend/ scripts/ --max-line-length=100

# Run tests
pytest tests/ -v --cov=backend

# Generate coverage report
pytest tests/ --cov=backend --cov-report=html

# Security check
bandit -r backend/

# Dependency check
pip-audit

# ============================================================================
# MONITORING & DEBUGGING
# ============================================================================

# Check API health
curl http://localhost:8000/health | python -m json.tool

# Get API statistics
curl http://localhost:8000/stats | python -m json.tool

# Test batch prediction
curl -X POST http://localhost:8000/batch-predict \
  -H "Content-Type: application/json" \
  -d '[{"text": "Great!"}, {"text": "Bad"}]'

# Check Redis
redis-cli
# Inside redis-cli:
# KEYS sentiment:*           # List all cached predictions
# GET sentiment:<hash>       # Get specific prediction
# DBSIZE                     # Total keys
# INFO memory                # Memory usage
# FLUSHDB                    # Clear cache

# View API logs (Docker)
docker logs sentiment-api -f

# View Redis logs (Docker)
docker logs sentiment-redis -f

# ============================================================================
# CLEANUP
# ============================================================================

# Remove virtual environment
rm -rf venv

# Stop Docker containers
docker stop sentiment-redis sentiment-api
docker rm sentiment-redis sentiment-api

# Remove Docker images
docker rmi sentimentvault:latest redis:7-alpine

# Remove models and data (⚠️ WARNING)
# rm -rf models/sentiment_model
# rm -rf data/

# ============================================================================
# HELPFUL REFERENCES
# ============================================================================

# View all endpoints
curl http://localhost:8000/openapi.json | python -m json.tool

# Check Python version
python --version

# List pip packages
pip list

# Verify CUDA (if using GPU)
python -c "import torch; print(torch.cuda.is_available())"

# Check model size
du -sh models/sentiment_model/

# Check dataset sizes
du -sh data/

# Count lines of code
find . -name "*.py" -type f | xargs wc -l

# ============================================================================
# PERFORMANCE TESTING
# ============================================================================

# Test single prediction latency
time curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Testing latency"}'

# Monitor system resources while running
watch -n 1 'curl -s http://localhost:8000/stats | python -m json.tool'

# ============================================================================
# DEPLOYMENT COMMANDS
# ============================================================================

# AWS EC2 deployment
# ssh -i key.pem ubuntu@instance-ip
# docker-compose -f docker/docker-compose.yml up -d

# Kubernetes deployment
# kubectl apply -f k8s/redis-deployment.yaml
# kubectl apply -f k8s/api-deployment.yaml
# kubectl port-forward svc/sentimentvault-api 8000:8000

# Docker Swarm deployment
# docker swarm init
# docker stack deploy -c docker/docker-compose.yml sentimentvault

# ============================================================================
# TROUBLESHOOTING
# ============================================================================

# If Redis connection fails
redis-cli ping
docker run -d -p 6379:6379 redis:7-alpine

# If port 8000 is in use
lsof -i :8000
kill -9 <PID>

# If Docker Compose fails
docker-compose down -v
docker-compose up --build

# If model not found
# Run Phase 2 notebook to train and save model

# Clear pip cache
pip cache purge

# Reinstall dependencies fresh
pip install --force-reinstall -r requirements.txt

# ============================================================================
# MONITORING DASHBOARDS
# ============================================================================

# Real-time stats in terminal
while true; do curl -s http://localhost:8000/stats | python -m json.tool; sleep 2; done

# Health check loop
while true; do curl -s http://localhost:8000/health | python -m json.tool; sleep 5; done

# ============================================================================
# DOCUMENTATION
# ============================================================================

# Read main README
less README.md

# Read API documentation
less API_DOCS.md

# Read deployment guide
less DEPLOYMENT.md

# Open API docs in browser
open http://localhost:8000/docs

# ============================================================================
# BACKUP & RESTORE
# ============================================================================

# Backup models
tar -czf backup_models.tar.gz models/

# Backup data
tar -czf backup_data.tar.gz data/

# Restore models
tar -xzf backup_models.tar.gz

# Restore data
tar -xzf backup_data.tar.gz

# ============================================================================
# QUICK REFERENCE
# ============================================================================

# All endpoints:
# POST /predict                - Single prediction
# POST /batch-predict          - Batch predictions  
# GET /health                  - Health check
# GET /stats                   - Statistics
# GET /docs                    - API documentation
# GET /openapi.json            - OpenAPI spec

# Typical flow:
# 1. activate venv
# 2. start redis
# 3. run Phase 1 notebook (EDA)
# 4. run Phase 2 notebook (training)
# 5. start API
# 6. run load test
# 7. push to GitHub

# Common issues & fixes:
# "Model not loaded" → Run Phase 2 notebook
# "Redis connection failed" → Start Redis
# "Port in use" → Kill existing process
# "Out of memory" → Reduce batch size in config

# ============================================================================
# SAVE THIS FILE
# ============================================================================

# Save as: SentimentVault/QUICK_COMMANDS.sh
# chmod +x QUICK_COMMANDS.sh
# ./QUICK_COMMANDS.sh  (view this file)

echo "SentimentVault Quick Command Reference"
echo "Copy commands from this file for quick execution"
echo ""
echo "Key commands:"
echo "  1. Setup: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
echo "  2. Redis: docker run -d -p 6379:6379 redis:7-alpine"
echo "  3. Phase 1: jupyter notebook notebooks/01_EDA_Data_Preparation.ipynb"
echo "  4. Phase 2: jupyter notebook notebooks/02_Model_Training.ipynb"
echo "  5. API: python -m uvicorn backend.main:app --reload"
echo "  6. Load Test: locust -f scripts/load_test.py -u 50 -r 5 -t 5m --host http://localhost:8000"
echo "  7. Git: git init && git add . && git commit -m 'Initial commit' && git push"
