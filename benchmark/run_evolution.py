import sys
import os
import subprocess
import time
import json

RESULTS_FILE = "benchmark_results.json"

def clear_results():
    if os.path.exists(RESULTS_FILE):
        os.remove(RESULTS_FILE)

def run_benchmark(message_count):
    print(f"--- Running benchmark for {message_count} messages ---")
    env = os.environ.copy()
    env["MESSAGE_COUNT"] = str(message_count)

    # Pulse
    print("Starting Pulse Consumer...")
    pulse_consumer = subprocess.Popen([sys.executable, "benchmark/pulse_consumer.py"], env=env)
    time.sleep(2) # Give consumer time to start
    
    print("Starting Pulse Producer...")
    subprocess.run([sys.executable, "benchmark/pulse_producer.py"], env=env, check=True)
    
    print("Waiting for Pulse Consumer to finish...")
    pulse_consumer.wait()

    # RabbitMQ
    print("Starting RabbitMQ Consumer...")
    rabbitmq_consumer = subprocess.Popen([sys.executable, "benchmark/rabbitmq_consumer.py"], env=env)
    time.sleep(2) # Give consumer time to start
    
    print("Starting RabbitMQ Producer...")
    subprocess.run([sys.executable, "benchmark/rabbitmq_producer.py"], env=env, check=True)
    
    print("Waiting for RabbitMQ Consumer to finish...")
    rabbitmq_consumer.wait()

def generate_summary():
    if not os.path.exists(RESULTS_FILE):
        print("No results found.")
        return

    with open(RESULTS_FILE, 'r') as f:
        data = json.load(f)

    # Organize data
    # Structure: { "Broker Role": { "x": [msg_counts], "y": [durations] } }
    series = {}
    
    for row in data:
        key = f"{row['broker']} {row['role']}"
        if key not in series:
            series[key] = {"x": [], "y": []}
        series[key]["x"].append(row["messages"])
        series[key]["y"].append(row["duration"])

    # Sort data points by message count and get common X axis
    x_values = sorted(list(set(d["messages"] for d in data)))
    
    # Ensure all series have values for all x_values (fill with 0 or None if missing, though our loop ensures they exist)
    # For Mermaid, we need aligned lists.
    
    print("\n### Evolution Benchmark Results")
    print("```mermaid")
    print("xychart-beta")
    print("    title \"Duration Evolution (Lower is Better)\"")
    print(f"    x-axis {json.dumps([str(x) for x in x_values])}")
    print("    y-axis \"Duration (s)\"")
    
    for key, values in series.items():
        # Sort values based on x_values to ensure alignment
        # Create a map of msg_count -> duration
        val_map = dict(zip(values["x"], values["y"]))
        aligned_y = [round(val_map.get(x, 0), 2) for x in x_values]
        
        print(f"    line {json.dumps(aligned_y)} \"{key}\"")
        
    print("```")

def main():
    clear_results()
    
    # 100k to 1M, step 100k
    for count in range(100000, 1100000, 100000):
        run_benchmark(count)
        time.sleep(1) # Cool down

    generate_summary()

if __name__ == "__main__":
    main()
