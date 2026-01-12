"""
SentimentVault Load Testing with Locust
Target: 5K+ predictions/hour with 50-100 concurrent users
This verifies the API can handle production traffic
"""

from locust import HttpUser, task, between, events
import random
import json
import time
from datetime import datetime

# Sample reviews for testing
SAMPLE_REVIEWS = [
    "This product is absolutely amazing! Highly recommended.",
    "Terrible quality, waste of money. Very disappointed.",
    "Excellent service and fast delivery. Very satisfied.",
    "Defective item arrived. Customer support was unhelpful.",
    "Love it! Exceeded my expectations. Will buy again.",
    "Worst purchase ever. Stopped working after one day.",
    "Good quality and reasonably priced. Happy customer.",
    "Broken on arrival. Still waiting for replacement.",
    "Outstanding value for money. Highly impressed.",
    "Complete disappointment. Returned immediately.",
    "Perfect! Does exactly what it promises.",
    "Cheap materials and poor craftsmanship.",
    "Best investment I made this year!",
    "Not worth the price tag at all.",
    "Fantastic customer service and great product!",
    "Failed after two weeks. Unacceptable quality.",
    "Impressive quality and durability.",
    "Regret buying this. Total waste of money.",
    "Exceeded expectations in every way!",
    "Avoid this product. Major issues after one week."
]

class SentimentVaultUser(HttpUser):
    """Simulated user for load testing"""
    
    wait_time = between(0.5, 2)  # Wait 0.5-2 seconds between requests
    
    def on_start(self):
        """Initialize user"""
        self.stats = {
            "requests": 0,
            "cache_hits": 0,
            "model_inference": 0,
            "errors": 0,
            "total_latency": 0
        }
    
    @task(1)
    def predict_sentiment(self):
        """Main task: predict sentiment"""
        review = random.choice(SAMPLE_REVIEWS)
        
        try:
            response = self.client.post(
                "/predict",
                json={"text": review},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.stats["requests"] += 1
                self.stats["total_latency"] += data.get("latency_ms", 0)
                
                if data.get("source") == "cache":
                    self.stats["cache_hits"] += 1
                else:
                    self.stats["model_inference"] += 1
            else:
                self.stats["errors"] += 1
        
        except Exception as e:
            self.stats["errors"] += 1
            print(f"Error: {str(e)}")
    
    @task(0.5)
    def check_health(self):
        """Periodic health checks"""
        self.client.get("/health")
    
    @task(0.1)
    def get_stats(self):
        """Get API stats"""
        try:
            response = self.client.get("/stats")
            if response.status_code == 200:
                stats = response.json()
                print(f"API Stats - Total: {stats['total_predictions']}, "
                      f"Cache hits: {stats['cache_hits']}, "
                      f"Hit rate: {stats['cache_hit_rate']*100:.1f}%")
        except Exception as e:
            pass
    
    def on_stop(self):
        """Print user stats on completion"""
        if self.stats["requests"] > 0:
            avg_latency = self.stats["total_latency"] / self.stats["requests"]
            print(f"\n--- User Stats ---")
            print(f"Total requests: {self.stats['requests']}")
            print(f"Cache hits: {self.stats['cache_hits']}")
            print(f"Model inferences: {self.stats['model_inference']}")
            print(f"Errors: {self.stats['errors']}")
            print(f"Average latency: {avg_latency:.2f}ms")

# Global stats tracking
@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Called when test starts"""
    print("\n" + "="*60)
    print("SENTIMENTVAULT LOAD TEST STARTING")
    print("="*60)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Target: 5K+ predictions/hour (~83 requests/minute)")
    print("="*60 + "\n")

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Called when test stops"""
    print("\n" + "="*60)
    print("SENTIMENTVAULT LOAD TEST COMPLETED")
    print("="*60)
    
    # Print summary stats
    total_requests = environment.stats.total.num_requests
    total_failures = environment.stats.total.num_failures
    avg_response_time = environment.stats.total.avg_response_time
    p99_response_time = environment.stats.total.get_response_time_percentile(0.99)
    
    print(f"Total requests: {total_requests}")
    print(f"Total failures: {total_failures}")
    print(f"Failure rate: {(total_failures/total_requests*100 if total_requests > 0 else 0):.2f}%")
    print(f"Average response time: {avg_response_time:.2f}ms")
    print(f"P99 response time: {p99_response_time:.2f}ms")
    
    # Calculate throughput
    if hasattr(environment, 'stats'):
        test_duration = (environment.stats.total.last_request_timestamp - 
                        environment.stats.total.start_time)
        if test_duration > 0:
            requests_per_hour = (total_requests / test_duration) * 3600
            print(f"Throughput: {requests_per_hour:.0f} requests/hour")
            print(f"Target met: {'✓ YES' if requests_per_hour >= 5000 else '✗ NO'}")
    
    print("="*60 + "\n")

# Configuration for load test execution
# Run with: locust -f locustfile.py -u 50 -r 5 -t 5m --host http://localhost:8000
