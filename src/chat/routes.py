from fastapi import APIRouter, HTTPException, status, Depends, WebSocket
from fastapi.responses import HTMLResponse
from src.authentication.models import UserCreate
from src.database import session_dep, get_session
from src.authentication import utils
from sqlmodel import Session
from typing import Annotated, Union
from src.authentication.utils import get_current_user
from src.chat.schemas import SendMessage
from src.authentication.models import User, get_user
from src.chat.models import ConversationParticipants
from src.chat.manager import get_or_create_conv, ConversationParticipants, get_chat_history, create_message
from src.kafka.producer import send_to_kafka
from src.config import TOPIC_NAME
router = APIRouter()


@router.post('/message')
def send_message(
    data: SendMessage, 
    session: session_dep,
    user: User= Depends(get_current_user)
):
    
    msg = create_message(data.model_dump(), user['id'], session)
    msg_dict = msg.model_dump()
    send_to_kafka(TOPIC_NAME, msg_dict)

    return msg


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

    return chat_history 

    


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@router.get("/")
async def get():
    return HTMLResponse(html)

@router.websocket('/ws')
async def get(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
   
        await websocket.send_text(f"You have a Message!: {data}")




    

