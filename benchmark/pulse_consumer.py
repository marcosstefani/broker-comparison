import time
import sys
import os
from pulse import consumer, run
from config import MESSAGE_COUNT, TOPIC_NAME
from report import save_result

count = 0
start_time = None

@consumer(TOPIC_NAME)
def handle(msg):
    global count, start_time
    if count == 0:
        start_time = time.time()
        print("Pulse Consumer: First message received.")
    
    count += 1
    if count % 1000 == 0:
        print(f"Consumed {count} messages", end='\r')

    if count >= MESSAGE_COUNT:
        end_time = time.time()
        duration = end_time - start_time
        print(f"\nPulse Consumer: {MESSAGE_COUNT} messages in {duration:.4f} seconds")
        save_result("Pulse", "Consumer", MESSAGE_COUNT, duration)
        # Force exit the process immediately, ensuring main thread also stops
        os._exit(0)

if __name__ == "__main__":
    print(f"Pulse Consumer: Waiting for {MESSAGE_COUNT} messages...")
    run()
