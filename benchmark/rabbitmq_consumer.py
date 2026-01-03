import time
import sys
import pika
from config import MESSAGE_COUNT, TOPIC_NAME

count = 0
start_time = None

def callback(ch, method, properties, body):
    global count, start_time
    
    if count == 0:
        start_time = time.time()
        print("RabbitMQ Consumer: First message received.")
    
    count += 1
    if count % 1000 == 0:
        print(f"Consumed {count} messages", end='\r')

    if count >= MESSAGE_COUNT:
        end_time = time.time()
        print(f"\nRabbitMQ Consumer: {MESSAGE_COUNT} messages in {end_time - start_time:.4f} seconds")
        ch.stop_consuming()

def run():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=pika.PlainCredentials('user', 'password'))
    )
    channel = connection.channel()

    channel.queue_declare(queue=TOPIC_NAME)

    print(f"RabbitMQ Consumer: Waiting for {MESSAGE_COUNT} messages...")
    channel.basic_consume(queue=TOPIC_NAME, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()
    connection.close()

if __name__ == "__main__":
    run()
