from json import dumps  
from kafka import KafkaProducer


producer = KafkaProducer(
    bootstrap_servers = ['localhost:9092'],
    value_serializer = lambda x:dumps(x).encode('utf-8') 
)

def send_to_kafka(topic: str, message: dict):
    # message["created_at"] = message["created_at"].isoformat()
    producer.send(topic, message)
    producer.flush  
