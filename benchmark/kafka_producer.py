import time
import json
from confluent_kafka import Producer
from config import MESSAGE_COUNT, TOPIC_NAME, PAYLOAD
from report import save_result

def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')

def run():
    conf = {'bootstrap.servers': 'localhost:9092'}
    producer = Producer(conf)

    print(f"Kafka Producer: Starting to produce {MESSAGE_COUNT} messages...")
    start = time.time()
    
    payload_bytes = json.dumps(PAYLOAD).encode('utf-8')
    
    for i in range(MESSAGE_COUNT):
        producer.produce(TOPIC_NAME, payload_bytes, callback=delivery_report)
        if i % 1000 == 0:
            producer.poll(0)
            print(f"Produced {i} messages", end='\r')
            
    producer.flush()
    end = time.time()
    duration = end - start
    print(f"\nKafka Producer: {MESSAGE_COUNT} messages in {duration:.4f} seconds")
    save_result("Kafka", "Producer", MESSAGE_COUNT, duration)

if __name__ == "__main__":
    run()
