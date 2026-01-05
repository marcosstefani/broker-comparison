import time
import sys
import os
from pulse import consumer, run, commit
from config import MESSAGE_COUNT, TOPIC_NAME
from report import save_result

count = 0
start_time = None

# Disable auto_commit to avoid a synchronous commit RPC for every single message.
# We will manually commit in batches, similar to how Kafka commits periodically.
@consumer(TOPIC_NAME, auto_commit=False)
def handle(msg):
    global count, start_time
    if count == 0:
        start_time = time.time()
        print("Pulse Consumer: First message received.")
    
    count += 1
    
    # Commit every 1000 messages to reduce network overhead
    if count % 1000 == 0:
        commit()
        if count % 100000 == 0:
            current_duration = time.time() - start_time
            print(f"Pulse Consumer: Reached {count} messages in {current_duration:.4f}s")
            save_result("Pulse", "Consumer", count, current_duration)

    if count >= MESSAGE_COUNT:
        # Final commit
        commit()
        
        end_time = time.time()
        duration = end_time - start_time
        print(f"\nPulse Consumer: {MESSAGE_COUNT} messages in {duration:.4f} seconds")
        save_result("Pulse", "Consumer", MESSAGE_COUNT, duration)
        # Force exit the process immediately
        os._exit(0)

if __name__ == "__main__":
    print(f"Pulse Consumer: Waiting for {MESSAGE_COUNT} messages...")
    run()
