from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from . import models
from .models import User
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
