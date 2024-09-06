import json
import os
import logging
from kafka import KafkaConsumer, KafkaProducer

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger('kafka').setLevel(logging.WARNING)

# Environment variables
KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'localhost:9092')
INPUT_TOPIC = os.getenv('INPUT_TOPIC', 'input-topic')
SUCCESS_TOPIC = os.getenv('SUCCESS_TOPIC', 'success-topic')
PERMANENT_FAILURE_TOPIC = os.getenv('PERMANENT_FAILURE_TOPIC', 'permanent-failure-topic')
TRANSIENT_FAILURE_TOPIC = os.getenv('TRANSIENT_FAILURE_TOPIC', 'transient-failure-topic')
GROUP_ID = os.getenv('GROUP_ID', 'demo-plugin-group')

# Set up Kafka consumer and producer
consumer = KafkaConsumer(
    INPUT_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    group_id=GROUP_ID,
    auto_offset_reset='earliest'
)

# Producer without serialization, to allow sending raw data
producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER)

def is_valid_json(message):
    try:
        json.loads(message)
        return True
    except ValueError:
        return False

def is_transient_failure():
    from datetime import datetime
    current_minute = datetime.now().minute
    return current_minute % 3 == 0

# Process messages from the input topic
for message in consumer:
    msg_value = message.value.decode('utf-8')
    logging.debug(f"Received message: {msg_value}")

    if is_transient_failure():
        # Send raw message back to the transient failure topic without altering its structure
        producer.send(TRANSIENT_FAILURE_TOPIC, message.value)
        logging.info(f"Transient failure: {msg_value}")
    elif is_valid_json(msg_value):
        # Send success message to the success topic
        producer.send(SUCCESS_TOPIC, json.dumps({'status': 'success', 'message': json.loads(msg_value)}).encode('utf-8'))
        logging.info(f"Message processed successfully: {msg_value}")
    else:
        # Send raw message to the permanent failure topic for invalid JSON
        producer.send(PERMANENT_FAILURE_TOPIC, message.value)
        logging.error(f"Permanent failure: {msg_value}")

    producer.flush()
