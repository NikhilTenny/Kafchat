import json
import asyncio
from src.config import TOPIC_NAME, REDIS_CHANNEL, KAFKA_SERVER, KAFKA_PORT, REDIS_SERVER, REDIS_PORT
from kafka import KafkaConsumer  
from src.database import consume_session
from redis import Redis


redis_client = Redis(host=REDIS_SERVER, port=REDIS_PORT, db=0)

my_consumer = KafkaConsumer(  
    bootstrap_servers = [f'{KAFKA_SERVER} : {KAFKA_PORT}'],  
    auto_offset_reset = 'earliest',  
    enable_auto_commit = True,  
    group_id = 'my-group',  
    value_deserializer = lambda x : json.loads(x.decode('utf-8'))  
    )  

my_consumer.subscribe([TOPIC_NAME])


async def consume_messages():
    
    for msg in my_consumer:
        print(msg.value)

        
        message = json.dumps(msg.value)
        redis_client.publish(REDIS_CHANNEL, message)

session = consume_session()


if __name__ == '__main__':
    asyncio.run(consume_messages())

