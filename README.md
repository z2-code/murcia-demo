# Kafka Demo with Transient and Permanent Failures

## Overview
This demo consists of multiple Docker containers simulating a Kafka-based system. The setup includes:
- A producer generating random measurements and sending them to an input topic.
- A plugin that processes the messages, sending valid messages to a success topic, and invalid or transiently failed messages to appropriate failure topics.
- A consumer that handles transient failures by retrying after a delay.
- Sinks that log messages from the success and permanent failure topics.

## Setup

### Prerequisites
- Docker
- Docker Compose

### Build the Containers
To build the Docker containers, run:
```sh
docker-compose build
```

### Run the Containers
To run all of the stack in the background:
```sh
docker-compose up -d
```

 To stop the system and rebuild just the plugin container, and then
 start it again::
```sh
docker-compose down
docker-compose build --no-cache plugin-container
docker-compose up -d
```

### Monitoring
To monitor all the containers, run:
```sh
docker-compose logs -f
```

## Plugin Container Requirements

The following are the requirements for creating a plugin that integrates with the Kafka-based system. The framework will handle Kafka setup, and the plugin container needs to conform to the following specifications:

### 1. **Environment Variables**
The framework will pass the following environment variables to the plugin container:

- `KAFKA_BROKER`: Address of the Kafka broker the plugin will communicate with.
- `INPUT_TOPIC`: The topic from which the plugin should consume input messages.
- `SUCCESS_TOPIC`: The topic where successfully processed messages should be published.
- `PERMANENT_FAILURE_TOPIC`: The topic for permanently failed messages.
- `TRANSIENT_FAILURE_TOPIC`: The topic for transient failures (for messages to be retried).
- `GROUP_ID`: Unique identifier for the Kafka consumer group used by the plugin.

### 2. **Message Handling**
- **Input**: The plugin should consume messages from the `INPUT_TOPIC`.
- **Output**:
  - Successfully processed messages should be sent to the `SUCCESS_TOPIC`.
  - Messages that encounter **permanent failures** should be sent to the `PERMANENT_FAILURE_TOPIC`.
  - Messages that encounter **transient failures** should be sent to the `TRANSIENT_FAILURE_TOPIC` for retrying.

The plugin should handle both **JSON** and **non-JSON** messages, based on the framework's needs.

### 3. **Scaling**
- The plugin **does not need to be asynchronous** but should be capable of handling a high message rate from `INPUT_TOPIC` by scaling horizontally.
- **Multiple instances** of the plugin container can be started in parallel to process messages more efficiently, with each instance being part of the same Kafka consumer group (`GROUP_ID`).
- Kafka will distribute the load evenly across all plugin instances consuming from the same topic.

### 4. **Graceful Shutdown**
- The plugin container must handle shutdown signals to ensure proper
  cleanup of resources and Kafka connections.
