import time
from pulse import Producer
from config import MESSAGE_COUNT, TOPIC_NAME, PAYLOAD

def run():
    # Assuming localhost defaults work as per README
    producer = Producer() 
    print(f"Pulse Producer: Starting to produce {MESSAGE_COUNT} messages...")
    start = time.time()
    for i in range(MESSAGE_COUNT):
        producer.send(TOPIC_NAME, PAYLOAD)
        if i % 1000 == 0:
            print(f"Produced {i} messages", end='\r')
    
    # Ensure all messages are sent (if async) - Pulse seems sync or fast enough, 
    # but if there's a flush, we should use it. README didn't mention flush.
    # producer.close() might flush.
    producer.close()
    
    end = time.time()
    print(f"\nPulse Producer: {MESSAGE_COUNT} messages in {end - start:.4f} seconds")

if __name__ == "__main__":
    run()
