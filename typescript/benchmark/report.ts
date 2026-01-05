import * as fs from 'fs';
import * as path from 'path';

const RESULTS_FILE = "benchmark_results.jsonl";

export function saveResult(broker: string, role: string, messages: number, duration: number) {
    const result = {
        broker,
        role,
        messages,
        duration,
        throughput: duration > 0 ? messages / duration : 0
    };
    
    // Append to file
    fs.appendFileSync(RESULTS_FILE, JSON.stringify(result) + "\n");
}
