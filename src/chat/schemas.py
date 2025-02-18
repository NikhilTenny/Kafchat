from pydantic import BaseModel


class SendMessage(BaseModel):
    receiver_id: int
    conv_id: int
    message_body: str
