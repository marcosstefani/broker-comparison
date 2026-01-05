import json
import os

RESULTS_FILE = "benchmark_results.jsonl"

def generate():
    if not os.path.exists(RESULTS_FILE):
        print("No results found.")
        return

    data = []
    with open(RESULTS_FILE, 'r') as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))

    print("### Benchmark Results")
    print("| Broker | Role | Messages | Duration (s) | Throughput (msg/s) |")
    print("|---|---|---|---|---|")
    
    for row in data:
        print(f"| {row['broker']} | {row['role']} | {row['messages']} | {row['duration']:.4f} | {row['throughput']:.2f} |")

    print("\n### Visualization")
    print("```mermaid")
    print("xychart-beta")
    print("    title \"Duration (seconds) - Lower is Better\"")
    
    labels = [f"{row['broker']} {row['role']}" for row in data]
    values = [round(row['duration'], 2) for row in data]
    
    print(f"    x-axis {json.dumps(labels)}")
    print(f"    y-axis \"Duration (s)\"")
    print(f"    bar {json.dumps(values)}")
    print("```")

if __name__ == "__main__":
    generate()
