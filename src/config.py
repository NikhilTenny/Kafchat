

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

ACCESS_TOKEN_EXPIRE_MINUTES = 300
SECRET_KEY = "5f54a5013ead93341595e0f201daabdfd66e47caaf6c805b836ba37cbfdf30294e755234a7ee7c40722760fbe0c0484092874105774877fc948110951b719985"
ALGORITHM = "HS256"

TOPIC_NAME = "text-message"

REDIS_SERVER = 'localhost'
REDIS_PORT = 6379
REDIS_CHANNEL = 'chat-message'

KAFKA_SERVER = 'localhost'
KAFKA_PORT = 9092