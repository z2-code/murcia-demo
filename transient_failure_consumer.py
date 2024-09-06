import time
import random
from kafka import KafkaConsumer, KafkaProducer
import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Set Kafka library logging to WARNING to suppress internal debug/info messages
logging.getLogger('kafka').setLevel(logging.WARNING)

# Environment variables
KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'localhost:9092')
INPUT_TOPIC = os.getenv('INPUT_TOPIC', 'input-topic')
TRANSIENT_FAILURE_TOPIC = os.getenv('TRANSIENT_FAILURE_TOPIC', 'transient-failure-topic')

# Set up Kafka consumer and producer
consumer = KafkaConsumer(
    TRANSIENT_FAILURE_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset='earliest'
)

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER
)

# Constantly listen for messages in the TRANSIENT_FAILURE_TOPIC
for message in consumer:
    # Log received message
    logging.info(f"Received transient failure: {message.value}")

    # Simulate delay before retrying
    delay = random.randint(30, 90)
    logging.info(f"Retrying message after {delay} seconds: {message.value}")
    time.sleep(delay)

    # Send the message as-is, without any assumptions about its format
    producer.send(INPUT_TOPIC, value=message.value)
    producer.flush()
    logging.debug(f"Retried message: {message.value}")
