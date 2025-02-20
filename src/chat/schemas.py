from typing import Optional
from pydantic import BaseModel


class SendMessage(BaseModel):
    receiver_id: int
    conv_id: Optional[int] = None
    body: str
