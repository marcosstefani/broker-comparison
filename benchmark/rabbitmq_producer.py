import time
import pika
import json
from config import MESSAGE_COUNT, TOPIC_NAME, PAYLOAD

def run():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=pika.PlainCredentials('user', 'password'))
    )
    channel = connection.channel()

    channel.queue_declare(queue=TOPIC_NAME)

    print(f"RabbitMQ Producer: Starting to produce {MESSAGE_COUNT} messages...")
    start = time.time()
    
    payload_bytes = json.dumps(PAYLOAD).encode('utf-8')

    for i in range(MESSAGE_COUNT):
        channel.basic_publish(exchange='', routing_key=TOPIC_NAME, body=payload_bytes)
        if i % 1000 == 0:
            print(f"Produced {i} messages", end='\r')

    connection.close()
    end = time.time()
    print(f"\nRabbitMQ Producer: {MESSAGE_COUNT} messages in {end - start:.4f} seconds")

if __name__ == "__main__":
    run()
