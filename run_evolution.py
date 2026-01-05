import sys
import os
import subprocess
import time
import json

# We will look for results in the subdirectories
RESULTS_FILES = ["python/benchmark_results.jsonl", "typescript/benchmark_results.jsonl"]

def clear_results():
    for f in RESULTS_FILES:
        if os.path.exists(f):
            os.remove(f)

def setup_typescript():
    print("--- Setting up TypeScript Environment ---")
    # Check if node_modules exists, if not install
    if not os.path.exists("typescript/node_modules"):
        subprocess.run(["npm", "install"], cwd="typescript", check=True)
    
    # Always build to ensure latest changes
    subprocess.run(["npm", "run", "build"], cwd="typescript", check=True)

def run_python_benchmark(message_count):
    print(f"--- Running Python Benchmark for {message_count} messages ---")
    env = os.environ.copy()
    env["MESSAGE_COUNT"] = str(message_count)
    
    # Pulse
    print("Starting Pulse Consumer (Python)...")
    pulse_consumer = subprocess.Popen([sys.executable, "benchmark/pulse_consumer.py"], env=env, cwd="python")
    time.sleep(2) # Give consumer time to start
    
    print("Starting Pulse Producer (Python)...")
    subprocess.run([sys.executable, "benchmark/pulse_producer.py"], env=env, check=True, cwd="python")
    
    print("Waiting for Pulse Consumer (Python) to finish...")
    pulse_consumer.wait()

    # RabbitMQ
    print("Starting RabbitMQ Consumer (Python)...")
    rabbitmq_consumer = subprocess.Popen([sys.executable, "benchmark/rabbitmq_consumer.py"], env=env, cwd="python")
    time.sleep(2) # Give consumer time to start
    
    print("Starting RabbitMQ Producer (Python)...")
    subprocess.run([sys.executable, "benchmark/rabbitmq_producer.py"], env=env, check=True, cwd="python")
    
    print("Waiting for RabbitMQ Consumer (Python) to finish...")
    rabbitmq_consumer.wait()

def run_ts_benchmark(message_count):
    print(f"--- Running TypeScript Benchmark for {message_count} messages ---")
    env = os.environ.copy()
    env["MESSAGE_COUNT"] = str(message_count)

    # Pulse
    print("Starting Pulse Consumer (TS)...")
    pulse_consumer = subprocess.Popen(["node", "dist/benchmark/pulse_consumer.js"], env=env, cwd="typescript")
    time.sleep(2) # Give consumer time to start
    
    print("Starting Pulse Producer (TS)...")
    subprocess.run(["node", "dist/benchmark/pulse_producer.js"], env=env, check=True, cwd="typescript")
    
    print("Waiting for Pulse Consumer (TS) to finish...")
    pulse_consumer.wait()

    # RabbitMQ
    print("Starting RabbitMQ Consumer (TS)...")
    rabbitmq_consumer = subprocess.Popen(["node", "dist/benchmark/rabbitmq_consumer.js"], env=env, cwd="typescript")
    time.sleep(2) # Give consumer time to start
    
    print("Starting RabbitMQ Producer (TS)...")
    subprocess.run(["node", "dist/benchmark/rabbitmq_producer.js"], env=env, check=True, cwd="typescript")
    
    print("Waiting for RabbitMQ Consumer (TS) to finish...")
    rabbitmq_consumer.wait()

def generate_summary():
    data = []
    for f_path in RESULTS_FILES:
        if os.path.exists(f_path):
            with open(f_path, 'r') as f:
                for line in f:
                    if line.strip():
                        data.append(json.loads(line))

    if not data:
        print("No results found.")
        return

    # Sort data points by message count and get common X axis
    x_values = sorted(list(set(d["messages"] for d in data)))
    
    # Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')

    # Generate Markdown Table
    print("### Evolution Benchmark Data")
    
    headers = [
        "Pulse Producer", "Pulse Consumer", "RabbitMQ Producer", "RabbitMQ Consumer",
        "Pulse (TS) Producer", "Pulse (TS) Consumer", "RabbitMQ (TS) Producer", "RabbitMQ (TS) Consumer"
    ]
    
    print("| Messages | " + " | ".join([h + " (s)" for h in headers]) + " |")
    print("|---|" + "|".join(["---"] * len(headers)) + "|")
    
    def get_duration(broker, role, msg_count):
        for row in data:
            if row['broker'] == broker and row['role'] == role and row['messages'] == msg_count:
                return f"{row['duration']:.4f}"
        return "-"

    for x in x_values:
        row_vals = [x]
        # Python
        row_vals.append(get_duration("Pulse", "Producer", x))
        row_vals.append(get_duration("Pulse", "Consumer", x))
        row_vals.append(get_duration("RabbitMQ", "Producer", x))
        row_vals.append(get_duration("RabbitMQ", "Consumer", x))
        # TS
        row_vals.append(get_duration("Pulse (TS)", "Producer", x))
        row_vals.append(get_duration("Pulse (TS)", "Consumer", x))
        row_vals.append(get_duration("RabbitMQ (TS)", "Producer", x))
        row_vals.append(get_duration("RabbitMQ (TS)", "Consumer", x))
        
        print("| " + " | ".join(str(v) for v in row_vals) + " |")

    # Generate Mermaid Charts
    # Chart 1: Producers
    print("\n### Producers Evolution")
    print("**Line 1:** Pulse (Py) | **Line 2:** RabbitMQ (Py) | **Line 3:** Pulse (TS) | **Line 4:** RabbitMQ (TS)")
    print("```mermaid")
    print("xychart-beta")
    print("    title \"Producers Duration (Lower is Better)\"")
    print(f"    x-axis {json.dumps([str(x) for x in x_values])}")
    print("    y-axis \"Duration (s)\"")
    
    # Python
    print(f"    line {json.dumps([round(float(get_duration('Pulse', 'Producer', x)), 2) if get_duration('Pulse', 'Producer', x) != '-' else 0 for x in x_values])}")
    print(f"    line {json.dumps([round(float(get_duration('RabbitMQ', 'Producer', x)), 2) if get_duration('RabbitMQ', 'Producer', x) != '-' else 0 for x in x_values])}")
    # TS
    print(f"    line {json.dumps([round(float(get_duration('Pulse (TS)', 'Producer', x)), 2) if get_duration('Pulse (TS)', 'Producer', x) != '-' else 0 for x in x_values])}")
    print(f"    line {json.dumps([round(float(get_duration('RabbitMQ (TS)', 'Producer', x)), 2) if get_duration('RabbitMQ (TS)', 'Producer', x) != '-' else 0 for x in x_values])}")
    print("```")

    # Chart 2: Consumers
    print("\n### Consumers Evolution")
    print("**Line 1:** Pulse (Py) | **Line 2:** RabbitMQ (Py) | **Line 3:** Pulse (TS) | **Line 4:** RabbitMQ (TS)")
    print("```mermaid")
    print("xychart-beta")
    print("    title \"Consumers Duration (Lower is Better)\"")
    print(f"    x-axis {json.dumps([str(x) for x in x_values])}")
    print("    y-axis \"Duration (s)\"")
    
    # Python
    print(f"    line {json.dumps([round(float(get_duration('Pulse', 'Consumer', x)), 2) if get_duration('Pulse', 'Consumer', x) != '-' else 0 for x in x_values])}")
    print(f"    line {json.dumps([round(float(get_duration('RabbitMQ', 'Consumer', x)), 2) if get_duration('RabbitMQ', 'Consumer', x) != '-' else 0 for x in x_values])}")
    # TS
    print(f"    line {json.dumps([round(float(get_duration('Pulse (TS)', 'Consumer', x)), 2) if get_duration('Pulse (TS)', 'Consumer', x) != '-' else 0 for x in x_values])}")
    print(f"    line {json.dumps([round(float(get_duration('RabbitMQ (TS)', 'Consumer', x)), 2) if get_duration('RabbitMQ (TS)', 'Consumer', x) != '-' else 0 for x in x_values])}")
    print("```")

def main():
    clear_results()
    setup_typescript()
    
    # Run once for 1M messages
    # The producers/consumers will log checkpoints every 100k
    run_python_benchmark(1000000)
    run_ts_benchmark(1000000)

    generate_summary()

if __name__ == "__main__":
    main()
