import time
import sys
from confluent_kafka import Consumer, KafkaError
from config import MESSAGE_COUNT, TOPIC_NAME

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

    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break

            if count == 0:
                start_time = time.time()
                print("Kafka Consumer: First message received.")

            count += 1
            if count % 1000 == 0:
                print(f"Consumed {count} messages", end='\r')

            if count >= MESSAGE_COUNT:
                end_time = time.time()
                print(f"\nKafka Consumer: {MESSAGE_COUNT} messages in {end_time - start_time:.4f} seconds")
                break
    finally:
        consumer.close()

if __name__ == "__main__":
    run()
