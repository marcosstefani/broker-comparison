import sys
import os
import subprocess
import time
import json

RESULTS_FILE = "benchmark_results.jsonl"

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

    data = []
    with open(RESULTS_FILE, 'r') as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))

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
    
    # Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')

    # Generate Markdown Table
    print("### Evolution Benchmark Data")
    print("| Messages | Pulse Producer (s) | Pulse Consumer (s) | RabbitMQ Producer (s) | RabbitMQ Consumer (s) |")
    print("|---|---|---|---|---|")
    
    # Helper to get duration
    def get_duration(broker, role, msg_count):
        for row in data:
            if row['broker'] == broker and row['role'] == role and row['messages'] == msg_count:
                return f"{row['duration']:.4f}"
        return "-"

    for x in x_values:
        pp = get_duration("Pulse", "Producer", x)
        pc = get_duration("Pulse", "Consumer", x)
        rp = get_duration("RabbitMQ", "Producer", x)
        rc = get_duration("RabbitMQ", "Consumer", x)
        print(f"| {x} | {pp} | {pc} | {rp} | {rc} |")

    # Generate Mermaid Charts
    # Chart 1: Producers
    print("\n### Producers Evolution")
    print("**Line 1:** Pulse Producer | **Line 2:** RabbitMQ Producer")
    print("```mermaid")
    print("xychart-beta")
    print("    title \"Producers Duration (Lower is Better)\"")
    print(f"    x-axis {json.dumps([str(x) for x in x_values])}")
    print("    y-axis \"Duration (s)\"")
    
    # Pulse Producer
    pp_data = [round(float(get_duration("Pulse", "Producer", x)), 2) for x in x_values]
    print(f"    line {json.dumps(pp_data)}")
    
    # RabbitMQ Producer
    rp_data = [round(float(get_duration("RabbitMQ", "Producer", x)), 2) for x in x_values]
    print(f"    line {json.dumps(rp_data)}")
    print("```")

    # Chart 2: Consumers
    print("\n### Consumers Evolution")
    print("**Line 1:** Pulse Consumer | **Line 2:** RabbitMQ Consumer")
    print("```mermaid")
    print("xychart-beta")
    print("    title \"Consumers Duration (Lower is Better)\"")
    print(f"    x-axis {json.dumps([str(x) for x in x_values])}")
    print("    y-axis \"Duration (s)\"")
    
    # Pulse Consumer
    pc_data = [round(float(get_duration("Pulse", "Consumer", x)), 2) for x in x_values]
    print(f"    line {json.dumps(pc_data)}")
    
    # RabbitMQ Consumer
    rc_data = [round(float(get_duration("RabbitMQ", "Consumer", x)), 2) for x in x_values]
    print(f"    line {json.dumps(rc_data)}")
    print("```")

def main():
    clear_results()
    
    # Run once for 1M messages
    # The producers/consumers will log checkpoints every 100k
    run_benchmark(1000000)

    generate_summary()

if __name__ == "__main__":
    main()
