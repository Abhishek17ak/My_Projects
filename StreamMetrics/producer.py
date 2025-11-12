from confluent_kafka import Producer
import json
import time

conf = {'bootstrap.servers': 'localhost:9092'}
producer = Producer(**conf)

def delivery_report(err, msg):
    if err:
        print(f'❌ Delivery failed: {err}')
    else:
        print(f'✅ Sent to {msg.topic()} [{msg.partition()}] @ {msg.offset()}')

# Prepare and send 5 events with a JSON structure
events = [
    {'event_type': 'cpu', 'value': 65.3, 'server': 'alpha', 'timestamp': int(time.time())},
    {'event_type': 'memory', 'value': 58.7, 'server': 'beta', 'timestamp': int(time.time())},
    {'event_type': 'cpu', 'value': 81.2, 'server': 'gamma', 'timestamp': int(time.time())},
    {'event_type': 'disk', 'value': 91.4, 'server': 'alpha', 'timestamp': int(time.time())},
    {'event_type': 'memory', 'value': 47.1, 'server': 'beta', 'timestamp': int(time.time())}
]

for event in events:
    producer.produce('test-metrics', value=json.dumps(event), callback=delivery_report)
    producer.poll(0)
    time.sleep(0.3)

producer.flush()
print('✅ All structured events sent!')
