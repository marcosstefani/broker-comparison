import time
import sys
import pika
from config import MESSAGE_COUNT, TOPIC_NAME
from report import save_result

count = 0
start_time = None

def callback(ch, method, properties, body):
    global count, start_time
    
    if count == 0:
        start_time = time.time()
        print("RabbitMQ Consumer: First message received.")
    
    count += 1
    if count % 100000 == 0:
        current_duration = time.time() - start_time
        print(f"RabbitMQ Consumer: Reached {count} messages in {current_duration:.4f}s")
        save_result("RabbitMQ", "Consumer", count, current_duration)

    if count >= MESSAGE_COUNT:
        end_time = time.time()
        duration = end_time - start_time
        print(f"\nRabbitMQ Consumer: {MESSAGE_COUNT} messages in {duration:.4f} seconds")
        save_result("RabbitMQ", "Consumer", MESSAGE_COUNT, duration)
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
