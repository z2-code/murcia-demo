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
PERMANENT_FAILURE_TOPIC = os.getenv('PERMANENT_FAILURE_TOPIC', 'permanent-failure-topic')

def create_consumer():
    try:
        consumer = KafkaConsumer(
            PERMANENT_FAILURE_TOPIC,
            bootstrap_servers=KAFKA_BROKER,
            auto_offset_reset='earliest'
        )
        logging.info(f"KafkaConsumer connected to {KAFKA_BROKER} and listening to topic '{PERMANENT_FAILURE_TOPIC}'")
        return consumer
    except Exception as e:
        logging.error(f"Failed to create KafkaConsumer: {str(e)}")
        raise

def process_messages(consumer):
    for message in consumer:
        try:
            msg_value = message.value.decode('utf-8')
            logging.error(f"Permanent failure: {msg_value}")
        except Exception as e:
            logging.error(f"Error processing message: {str(e)}")

if __name__ == "__main__":
    try:
        consumer = create_consumer()
        process_messages(consumer)
    except Exception as e:
        logging.critical(f"Application failed: {str(e)}")
