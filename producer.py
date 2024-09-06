import time
import random
from kafka import KafkaProducer
import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Set Kafka library logging to WARNING to suppress internal debug/info messages
logging.getLogger('kafka').setLevel(logging.WARNING)

KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'localhost:9092')
INPUT_TOPIC = os.getenv('INPUT_TOPIC', 'input-topic')

# Kafka producer without forcing JSON serialization
producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER)

def generate_measurement():
    """Randomly generate a valid or invalid message"""
    if random.random() < 0.25:  # 25% chance of generating an invalid (non-JSON) message
        invalid_message = "This is not JSON!"
        logging.debug(f"Generated invalid message: {invalid_message}")
        return invalid_message.encode('utf-8')  # Send raw string as bytes
    else:
        valid_message = '{"value": %d, "timestamp": %f}' % (random.randint(0, 9), time.time())
        logging.debug(f"Generated valid JSON message: {valid_message}")
        return valid_message.encode('utf-8')  # Send valid JSON as bytes

while True:
    measurement = generate_measurement()
    producer.send(INPUT_TOPIC, value=measurement)
    logging.info(f"Produced measurement: {measurement}")
    producer.flush()
    time.sleep(random.randint(5, 30))
