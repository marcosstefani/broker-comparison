import json
import os

RESULTS_FILE = "benchmark_results.jsonl"

def save_result(broker, role, messages, duration):
    result = {
        "broker": broker,
        "role": role,
        "messages": messages,
        "duration": duration,
        "throughput": messages / duration if duration > 0 else 0
    }
    
    with open(RESULTS_FILE, 'a') as f:
        f.write(json.dumps(result) + "\n")
