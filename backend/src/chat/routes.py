from typing import List
from fastapi import APIRouter, HTTPException, WebSocketDisconnect, status, Depends, WebSocket
from src.authentication.utils import get_current_user
from src.chat.schemas import SendMessage
from src.authentication.models import User, get_user
from src.chat.models import ConversationParticipants
from src.chat.manager import get_or_create_conv, ConversationParticipants, get_chat_history
from src.kafka.producer import send_to_kafka
from src.chat.socket_manager import SocketManager
from src.chat.manager import create_message 
from src.database import consume_session, session_dep
from src.config import TOPIC_NAME, REDIS_CHANNEL
from src.redis import redis_client
import json


router = APIRouter()

pubsub = redis_client.pubsub()

sock_manager = SocketManager()

@router.post('/message')
async def send_message(
    data: SendMessage, 
    session: session_dep,
    user: User= Depends(get_current_user)
):
    
    msg_data: dict = data.model_dump()
    msg_data['user_data'] = user

    send_to_kafka(TOPIC_NAME, msg_data)
    return {"message", "Message send successfully"}


@router.get('/chat-history')
def chat_history(
    receiver_uname: str,
    session: session_dep,
    user: User= Depends(get_current_user)
):
    receiver: User = get_user(session, receiver_uname)
    if not receiver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Receiver not found.")
    
    conversation: ConversationParticipants = get_or_create_conv(user, receiver.model_dump(), session)
    if not conversation:
        raise HTTPException(status_code=500, detail="Failed to fetch conversation.")

    chat_history = get_chat_history(conversation.conv_id, session)
    response = {
        "conv_id": conversation.conv_id,
        "chat_history": chat_history
    }

    return response 


active_connections: List[WebSocket] = []

@router.websocket('/ws/{user_id}')
async def get(websocket: WebSocket, user_id: int):
    await sock_manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_json()
    except WebSocketDisconnect:
        sock_manager.disconnect(user_id)




async def listen_to_redis():
    session = consume_session()
    await pubsub.subscribe(REDIS_CHANNEL)
        
    async for message in pubsub.listen():
        print(message)
        if message['type'] == 'message':
            try:
                msg_data = json.loads(message["data"].decode('utf-8'))
                user_data = msg_data["user_data"]
                del msg_data["user_data"]
                
                msg = create_message(msg_data, user_data, session)
                await sock_manager.personal_msg(msg_data, user_data['id'])
            except Exception as e:
                print(e)
                




    

