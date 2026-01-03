import time
from pulse import Producer
from config import MESSAGE_COUNT, TOPIC_NAME, PAYLOAD
from report import save_result

def run():
    # Assuming localhost defaults work as per README
    producer = Producer() 
    print(f"Pulse Producer: Starting to produce {MESSAGE_COUNT} messages...")
    
    start = time.time()
    
    # Use streaming publish for high throughput
    def message_generator():
        for i in range(MESSAGE_COUNT):
            if i % 1000 == 0:
                print(f"Generating {i} messages", end='\r')
            yield (TOPIC_NAME, PAYLOAD)

    producer.stream_send(message_generator())

    producer.close()
    
    end = time.time()
    duration = end - start
    print(f"\nPulse Producer: {MESSAGE_COUNT} messages in {duration:.4f} seconds")
    save_result("Pulse", "Producer", MESSAGE_COUNT, duration)

if __name__ == "__main__":
    run()
