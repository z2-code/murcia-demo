from kafka import KafkaConsumer
import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set Kafka library logging to WARNING to suppress internal debug/info messages
logging.getLogger('kafka').setLevel(logging.WARNING)

# Environment variables
KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'localhost:9092')
SUCCESS_TOPIC = os.getenv('SUCCESS_TOPIC', 'success-topic')

def create_consumer():
    try:
        consumer = KafkaConsumer(
            SUCCESS_TOPIC,
            bootstrap_servers=KAFKA_BROKER,
            auto_offset_reset='earliest'
        )
        logging.info(f"KafkaConsumer connected to {KAFKA_BROKER} and listening to topic '{SUCCESS_TOPIC}'")
        return consumer
    except Exception as e:
        logging.error(f"Failed to create KafkaConsumer: {str(e)}")
        raise

def process_messages(consumer):
    for message in consumer:
        msg_value = message.value.decode('utf-8')
        logging.info(f"Success: {msg_value}")

if __name__ == "__main__":
    try:
        consumer = create_consumer()
        process_messages(consumer)
    except Exception as e:
        logging.critical(f"Application failed: {str(e)}")
