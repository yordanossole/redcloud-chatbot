from fastapi import Depends
from fastapi.security import HTTPBasic
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import secrets
from ..config import SESSION_EXPIRY_MINUTES

from ..custom_exceptions import GeneralException
from ..database.db import get_user, update_user_session, create_user
from ..database.models import get_db


secutiry = HTTPBasic()

def verify_user(db: Session, username: str, password: str):
    user = get_user(db=db, username = username)
    
    if user and str(user.password) == password:
        return True
    
    return False

def create_session_token(db: Session, username: str):
    token = secrets.token_urlsafe(32)
    expiry = datetime.now() + timedelta(minutes=SESSION_EXPIRY_MINUTES)

    user = get_user(db, username=username)
    user = update_user_session(db=db, user=user, session_token=token, token_expiry=expiry)

    return token

def validate_session_token(db: Session, username: str, token: str):
    user = get_user(db = db, username = username)

    if not user:
        return False
    
    stored_token = user.session_token
    expiry = user.token_expiry

    if not str(stored_token) or not expiry:
        return False
    
    if secrets.compare_digest(token, stored_token) and datetime.now() < expiry:
        return True
    
    return False

def delete_session(db: Session, session_token: str):
    user = get_user(db=db, session_token=session_token)
    
    if user:
        return update_user_session(db= db, user=user) # this deletes the session_token and the token_expiry
    else:
        raise GeneralException(message="User session not found")

def create_new_user(db: Session, username: str, password: str):
    user = create_user(db=db, username=username, password=password)
    return user
