import time
import sys
from pulse import consumer, run
from config import MESSAGE_COUNT, TOPIC_NAME

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
        print(f"\nPulse Consumer: {MESSAGE_COUNT} messages in {end_time - start_time:.4f} seconds")
        sys.exit(0)

if __name__ == "__main__":
    print(f"Pulse Consumer: Waiting for {MESSAGE_COUNT} messages...")
    run()
