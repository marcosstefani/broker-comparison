import time
import concurrent.futures
from pulse import Producer
from config import MESSAGE_COUNT, TOPIC_NAME, PAYLOAD
from report import save_result

def run():
    # Assuming localhost defaults work as per README
    producer = Producer() 
    print(f"Pulse Producer: Starting to produce {MESSAGE_COUNT} messages...")
    
    start = time.time()
    
    # Use a thread pool to simulate async/concurrent production
    # This helps saturate the broker better than a single synchronous thread
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = []
        for i in range(MESSAGE_COUNT):
            futures.append(executor.submit(producer.send, TOPIC_NAME, PAYLOAD))
            
            if i % 1000 == 0:
                print(f"Scheduled {i} messages", end='\r')
        
        # Wait for all to complete
        concurrent.futures.wait(futures)

    producer.close()
    
    end = time.time()
    duration = end - start
    print(f"\nPulse Producer: {MESSAGE_COUNT} messages in {duration:.4f} seconds")
    save_result("Pulse", "Producer", MESSAGE_COUNT, duration)

if __name__ == "__main__":
    run()
