import time
import pika
import json
from config import MESSAGE_COUNT, TOPIC_NAME, PAYLOAD
from report import save_result

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
    duration = end - start
    print(f"\nRabbitMQ Producer: {MESSAGE_COUNT} messages in {duration:.4f} seconds")
    save_result("RabbitMQ", "Producer", MESSAGE_COUNT, duration)

if __name__ == "__main__":
    run()
