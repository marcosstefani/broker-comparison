# Broker Comparison Benchmark

This repository contains a performance comparison between **Pulse**, **Kafka**, and **RabbitMQ**.

The goal is to measure the time required to consume a fixed load of messages in each of the brokers.

## Prerequisites

- Docker and Docker Compose
- Python 3.8+

## Environment Setup

1. **Start the Brokers**
   
   Start the Pulse, Kafka, and RabbitMQ containers:
   ```bash
   docker-compose up -d
   ```

2. **Prepare the Python Environment**

   Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## Running the Tests

The testing strategy consists of two steps for each broker:
1. **Producer**: Sends a fixed amount of messages (configured in `benchmark/config.py`) to the broker.
2. **Consumer**: Reads the messages and measures the time elapsed between the first and the last message received.

You can adjust the message count and payload size in `benchmark/config.py`.

### 1. Pulse

**Terminal 1 (Consumer - Start first or later, Pulse persists):**
```bash
python benchmark/pulse_consumer.py
```

**Terminal 2 (Producer):**
```bash
python benchmark/pulse_producer.py
```

### 2. Kafka

**Terminal 1 (Consumer):**
```bash
python benchmark/kafka_consumer.py
```

**Terminal 2 (Producer):**
```bash
python benchmark/kafka_producer.py
```

### 3. RabbitMQ

**Terminal 1 (Consumer):**
```bash
python benchmark/rabbitmq_consumer.py
```

**Terminal 2 (Producer):**
```bash
python benchmark/rabbitmq_producer.py
```

## Cleanup

To stop and remove the containers:
```bash
docker-compose down
```
