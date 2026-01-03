import json
import os

RESULTS_FILE = "benchmark_results.json"

def save_result(broker, role, messages, duration):
    result = {
        "broker": broker,
        "role": role,
        "messages": messages,
        "duration": duration,
        "throughput": messages / duration if duration > 0 else 0
    }
    
    data = []
    if os.path.exists(RESULTS_FILE):
        try:
            with open(RESULTS_FILE, 'r') as f:
                data = json.load(f)
        except:
            pass
    
    data.append(result)
    
    with open(RESULTS_FILE, 'w') as f:
        json.dump(data, f, indent=2)
