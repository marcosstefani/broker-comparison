import time
import sys
from confluent_kafka import Consumer, KafkaError
from config import MESSAGE_COUNT, TOPIC_NAME
from report import save_result

def run():
    conf = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'benchmark_group',
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(conf)
    consumer.subscribe([TOPIC_NAME])

    count = 0
    start_time = None
    
    print(f"Kafka Consumer: Waiting for {MESSAGE_COUNT} messages...")

    # Wait for topic/messages to be available
    retries = 10
    while retries > 0:
        msg = consumer.poll(1.0)
        if msg is None:
            retries -= 1
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                # Ignore initial errors like unknown topic while it's being created/propagated
                print(f"Kafka Warning: {msg.error()}")
                continue
        
        # If we got here, we have a valid message
        if count == 0:
            start_time = time.time()
            print("Kafka Consumer: First message received.")
        
        count += 1
        break # Exit retry loop and enter main loop

    if count == 0:
        print("Kafka Consumer: No messages received after retries.")
        return

    try:
        while True:
            # We already have one message if we broke the loop above, but let's simplify logic
            # by just continuing the loop. Wait, we consumed one.
            
            if count % 1000 == 0:
                print(f"Consumed {count} messages", end='\r')

            if count >= MESSAGE_COUNT:
                end_time = time.time()
                duration = end_time - start_time
                print(f"\nKafka Consumer: {MESSAGE_COUNT} messages in {duration:.4f} seconds")
                save_result("Kafka", "Consumer", MESSAGE_COUNT, duration)
                break

            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break
            
            count += 1
    finally:
        consumer.close()

if __name__ == "__main__":
    run()
