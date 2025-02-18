

from sqlmodel import Session, select
from fastapi import HTTPException
from src.chat.models import Conversation, ConversationParticipants, Messages
from src.chat.schemas import SendMessage


def create_conversation(name: str, session: Session):
    try:
        if not name or len(name) > 255:
            raise ValueError("Conversation name is required and must be <= 255 characters.")
        conv = Conversation(name=name)
        session.add(conv)
        session.commit()
        session.refresh(conv)
        return conv
    except Exception as e:
        session.rollback()
        raise RuntimeError(f"Unexpected error: {str(e)}")


def create_conv_participants(user_id: int, conv_id: int, session: Session):
    try:
        conv_ptcpts = ConversationParticipants(user_id=user_id, conv_id=conv_id)
        session.add(conv_ptcpts)
        session.commit()
        session.refresh(conv_ptcpts)
        return conv_ptcpts
    except Exception as e:
        session.rollback()
        raise RuntimeError(f"Unexpected error: {str(e)}")


def create_new_chat(sender: dict, receiver: dict, session: Session):
    """
        Creates a new record in Conversation table.
        Create records for both sender and receiver.
        Used when starting a new chat
    """
    conv_name = f"{sender['user']}_{receiver['user_name']}"
    conversation = create_conversation(conv_name, session)
    if not conversation:
        raise RuntimeError("Failed to create conversation.")

    create_conv_participants(sender["id"], conversation.id, session)
    return create_conv_participants(receiver["id"], conversation.id, session)


def get_or_create_conv(sender: dict, receiver: dict, session: Session):
    try:
        shared_conversation = session.exec(
            select(ConversationParticipants).filter(
                ConversationParticipants.user_id == sender["id"],
                ConversationParticipants.conv_id.in_(
                    select(ConversationParticipants.conv_id).filter(
                        ConversationParticipants.user_id == receiver["id"]
                    )
                )
            )
        ).first()

        if shared_conversation:
            return shared_conversation

        # If no existing conversation, create a new one
        new_chat = create_new_chat(sender, receiver, session)
        return new_chat
    except Exception as e:
        raise RuntimeError(f"Error Occured: {str(e)}")




def get_chat_history(conv_id: int, session: Session):
    try:
        chat_msgs = session.exec(
            select(Messages).filter(
                Messages.conv_id == conv_id
            ).order_by(Messages.created_at)
        ).all()

        if not chat_msgs:
            raise HTTPException(status_code=404, detail="No messages found for this conversation.")

        return chat_msgs

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch chat history: {str(e)}")



def create_message(msg_data: SendMessage, user_id: int, session: Session):
    try:
        msg = Messages(
            body = msg_data["message_body"],
            sender_id=user_id,
            conv_id=msg_data["conv_id"]
        )
        session.add(msg)
        session.commit()
        session.refresh(msg)
        return msg
    except Exception as e:
        session.rollback()
        raise RuntimeError(f"Unexpected error: {str(e)}")

