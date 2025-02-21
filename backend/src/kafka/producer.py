from json import dumps  
from kafka import KafkaProducer
from src.config import KAFKA_SERVER, KAFKA_PORT
producer = KafkaProducer(
    bootstrap_servers = [f'{KAFKA_SERVER}:{KAFKA_PORT}'],
    value_serializer = lambda x:dumps(x).encode('utf-8') 
)
def send_to_kafka(topic: str, message: dict):
    # message["created_at"] = message["created_at"].isoformat()
    producer.send(topic, message)
    producer.flush  
