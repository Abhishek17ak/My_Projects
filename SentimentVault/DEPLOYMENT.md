# Deployment Guide

## Deployment Options

SentimentVault can be deployed in multiple ways depending on your infrastructure and requirements.

## 1. Local Development

### Requirements
- Python 3.10+
- Redis
- 8GB RAM

### Setup
```bash
# Clone and setup
git clone https://github.com/Abhishek17ak/SentimentVault.git
cd SentimentVault

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start Redis
redis-server

# Run EDA notebook
jupyter notebook notebooks/01_EDA_Data_Preparation.ipynb

# Run training notebook
jupyter notebook notebooks/02_Model_Training.ipynb

# Start API
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

## 2. Docker (Single Machine)

### Requirements
- Docker
- Docker Compose
- 10GB disk space (for model + Redis)

### Deployment
```bash
# Build and start
docker-compose -f docker/docker-compose.yml up --build -d

# Verify
docker-compose ps
curl http://localhost:8000/health

# View logs
docker-compose logs -f api

# Stop
docker-compose down
```

### Docker Compose Services
- **API:** Port 8000
- **Redis:** Port 6379
- **Health Checks:** Automatic

## 3. Docker Swarm

### Requirements
- Docker Swarm initialized
- 3+ nodes (for HA)

### Deployment
```bash
# Initialize Swarm (on first node)
docker swarm init

# Join workers to swarm
docker swarm join --token SWMTKN-... <manager-ip>:2377

# Deploy stack
docker stack deploy -c docker/docker-compose.yml sentimentvault

# Check status
docker stack services sentimentvault

# Scale replicas
docker service scale sentimentvault_api=3

# Remove stack
docker stack rm sentimentvault
```

## 4. Kubernetes

### Requirements
- kubectl configured
- Kubernetes cluster (1.20+)
- Helm 3.0+

### Helm Deployment (Recommended)
```bash
# Add repository (when chart is available)
helm repo add sentimentvault https://charts.sentimentvault.dev
helm repo update

# Install
helm install sentimentvault sentimentvault/sentimentvault \
  --set image.tag=1.0.0 \
  --set replicas=3 \
  --set redis.enabled=true

# Verify
kubectl get pods -l app=sentimentvault
kubectl port-forward svc/sentimentvault-api 8000:8000

# Check logs
kubectl logs -l app=sentimentvault -f

# Upgrade
helm upgrade sentimentvault sentimentvault/sentimentvault \
  --set image.tag=1.0.1

# Uninstall
helm uninstall sentimentvault
```

### Manual Kubernetes (YAML)
```bash
# Create namespace
kubectl create namespace sentimentvault

# Create Redis ConfigMap
kubectl apply -f k8s/redis-configmap.yaml -n sentimentvault

# Deploy Redis
kubectl apply -f k8s/redis-deployment.yaml -n sentimentvault

# Deploy API
kubectl apply -f k8s/api-deployment.yaml -n sentimentvault

# Expose API
kubectl apply -f k8s/api-service.yaml -n sentimentvault

# Check status
kubectl get all -n sentimentvault
```

**Kubernetes Sample Files (k8s/ directory):**
```yaml
# k8s/api-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sentimentvault-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: sentimentvault
  template:
    metadata:
      labels:
        app: sentimentvault
    spec:
      containers:
      - name: api
        image: sentimentvault:1.0.0
        ports:
        - containerPort: 8000
        env:
        - name: REDIS_HOST
          value: sentimentvault-redis
        resources:
          requests:
            cpu: 500m
            memory: 2Gi
          limits:
            cpu: 1000m
            memory: 4Gi
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
```

## 5. AWS Deployment

### Using EC2 + ElastiCache + ALB
```bash
# 1. Launch EC2 instance
# - AMI: Ubuntu 22.04 LTS
# - Instance: t3.large
# - Security Group: Allow 8000, 22

# 2. SSH into instance
ssh -i key.pem ubuntu@instance-ip

# 3. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 4. Clone repository
git clone https://github.com/Abhishek17ak/SentimentVault.git
cd SentimentVault

# 5. Configure Redis endpoint (ElastiCache)
# Edit .env:
# REDIS_HOST=redis-cluster.xxxxx.ng.0001.use1.cache.amazonaws.com
# REDIS_PORT=6379

# 6. Start API container
docker run -d \
  --name sentiment-api \
  -p 8000:8000 \
  --env-file .env \
  -v $(pwd)/models:/app/models \
  sentimentvault:latest

# 7. Configure ALB target group
# - Protocol: HTTP
# - Port: 8000
# - Health check path: /health
```

### Using AWS ECS + ECR
```bash
# 1. Create ECR repository
aws ecr create-repository --repository-name sentimentvault

# 2. Push image
docker tag sentimentvault:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/sentimentvault:latest
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/sentimentvault:latest

# 3. Create ECS task definition (see ecs-task-definition.json)

# 4. Create ECS service
aws ecs create-service \
  --cluster sentiment-cluster \
  --service-name sentimentvault \
  --task-definition sentimentvault:1 \
  --desired-count 3 \
  --launch-type EC2
```

## 6. Google Cloud Deployment

### Using Google Cloud Run
```bash
# 1. Build and push to Artifact Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/sentimentvault:latest

# 2. Deploy to Cloud Run
gcloud run deploy sentimentvault \
  --image gcr.io/PROJECT_ID/sentimentvault:latest \
  --region us-central1 \
  --memory 4Gi \
  --cpu 2 \
  --set-env-vars REDIS_HOST=redis-host \
  --allow-unauthenticated

# 3. Check deployment
gcloud run services list
gcloud run services describe sentimentvault --region us-central1
```

### Using GKE
```bash
# 1. Create GKE cluster
gcloud container clusters create sentiment-cluster \
  --num-nodes 3 \
  --machine-type n1-standard-2

# 2. Install Helm chart
helm install sentimentvault sentimentvault/sentimentvault

# 3. Expose via LoadBalancer
kubectl expose deployment sentimentvault-api \
  --type LoadBalancer \
  --port 80 \
  --target-port 8000
```

## 7. Azure Deployment

### Using Azure Container Instances
```bash
# 1. Push to Azure Container Registry
az acr build --registry sentimentvault \
  --image sentimentvault:latest .

# 2. Deploy container
az container create \
  --resource-group sentiment-rg \
  --name sentimentvault-api \
  --image sentimentvault.azurecr.io/sentimentvault:latest \
  --ports 8000 \
  --environment-variables REDIS_HOST=redis-host \
  --cpu 2 --memory 4
```

### Using Azure Kubernetes Service (AKS)
```bash
# 1. Create AKS cluster
az aks create \
  --resource-group sentiment-rg \
  --name sentiment-cluster \
  --node-count 3 \
  --vm-set-type VirtualMachineScaleSets

# 2. Deploy with Helm
helm install sentimentvault sentimentvault/sentimentvault

# 3. Monitor
az aks show --resource-group sentiment-rg --name sentiment-cluster
```

## 8. Heroku Deployment

### Via Procfile
```bash
# 1. Create Procfile
echo "web: uvicorn backend.main:app --host 0.0.0.0 --port \$PORT" > Procfile

# 2. Create app
heroku create sentimentvault

# 3. Add Redis addon
heroku addons:create heroku-redis

# 4. Deploy
git push heroku main

# 5. Check logs
heroku logs --tail
```

## Production Checklist

- [ ] Environment variables configured (DEBUG=False)
- [ ] External Redis instance configured
- [ ] SSL/TLS certificates installed
- [ ] Logging to external service
- [ ] Monitoring/alerting setup
- [ ] Database backups configured
- [ ] Rate limiting enabled
- [ ] Authentication/authorization implemented
- [ ] Load balancer configured
- [ ] Health checks verified
- [ ] Auto-scaling configured
- [ ] Disaster recovery plan

## Monitoring & Observability

### Prometheus Metrics
```bash
# Endpoint: /metrics
# Export format: Prometheus-compatible
```

### Logging
```bash
# CloudWatch
docker logs $(docker ps -q)

# Stackdriver
gcloud logging read --limit 50

# ELK Stack
# Configure logstash to forward logs
```

### Alerts
```
- API latency > 100ms
- Cache hit rate < 50%
- Error rate > 1%
- Redis memory > 80%
- Model inference > 5 seconds
```

## Rollback Strategy

```bash
# For Docker
docker rollback sentimentvault_api v1.0.0

# For Kubernetes
kubectl rollout undo deployment/sentimentvault-api

# For ECS
aws ecs update-service \
  --cluster sentiment-cluster \
  --service sentimentvault \
  --task-definition sentimentvault:previous
```

## Cost Optimization

1. **Compute:** Use spot instances for non-critical environments
2. **Storage:** Archive old logs, compress model files
3. **Network:** Use CDN for static content
4. **Cache:** Optimize Redis TTL values
5. **Scaling:** Auto-scale based on actual load

---

**Need help?** See CONTRIBUTING.md or contact support@sentimentvault.dev
