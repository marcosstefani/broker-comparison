import os

# Configuration with Environment Variable overrides
MESSAGE_COUNT = int(os.getenv("MESSAGE_COUNT", "10000"))
TOPIC_NAME = os.getenv("TOPIC_NAME", "benchmark_test")
PAYLOAD = {"data": "x" * 100} # 100 bytes payload
