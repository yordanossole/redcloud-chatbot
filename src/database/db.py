from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from . import models
from .models import User, Chat, Message
from ..custom_exceptions import GeneralException

def get_user(db: Session, username: str = "", session_token: str = ""):
    if username:
        return db.query(models.User).filter(models.User.username == username).first()
    elif session_token:
        return db.query(models.User).filter(models.User.session_token == session_token).first()
    raise GeneralException(message="Unable to find the user")


def create_user(db: Session, username: str, password: str):
    user = (db.query(models.User)
            .filter(models.User.username == username)
            .first())
    
    if user:
        raise GeneralException(message="User already exists could not sign-up")

    user = models.User(username=username, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user


def update_user_session(db: Session, user: User, session_token: str = "", token_expiry: Optional[datetime] = None):
    user.session_token = session_token
    user.token_expiry = token_expiry
    db.commit()
    db.refresh(user)

    return user


# Chat 
def get_chat(db: Session, chat_id: int, user: User):
    chat = db.query(models.Chat).filter_by(id=chat_id, user=user).first()
    if not chat:
        raise GeneralException(message="Chat not found")
    return chat

def get_all_chats(db: Session, user: User):
    chats = db.query(models.Chat).filter_by(user=user).all()
    if not chats:
        raise GeneralException(message="No chat found")   
    return chats

def create_new_chat(db: Session, user: User):
    new_chat = Chat()
    new_chat.user = user
    new_chat.user_id = user.id
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    return new_chat

def update_chat(db: Session, chat: Chat, user: User):
    pass

def delete_chat(db: Session, chat: Chat):
    db.delete(chat)
    db.commit()

# messages
def get_messages(db: Session, chat: Chat):
    messages = db.query(models.Message).filter_by(chat=chat).all()
    # if not messages:
    #     raise GeneralException(message="No chat history")
    return messages

def create_message(db: Session, chat: Chat, role: str, text: str):
    new_message = Message(
        role= role,
        text=text,
        chat=chat,
        chat_id=chat.id
    )

    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message