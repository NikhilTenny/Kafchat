from fastapi import APIRouter, HTTPException, status, Depends
from src.authentication.models import UserCreate, list_users
from src.database import session_dep, get_session
from src.authentication import utils
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from typing import Annotated, List, Union
from src.authentication.utils import get_current_user

from src.authentication.models import User, UserPublic, authenticate_user, check_if_user_exists
router = APIRouter()


@router.post('/sign-up', response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def user_signup(
    user: UserCreate, 
    session: session_dep, 

):
    """ Create and store new user in db if not already exists

    Args:
        user (UserCreate): _description_
        session (session_dep): _description_

    Raises:
        HTTPException: _description_

    Returns:
        UserPublic: _description_
    """
    if check_if_user_exists(user.user_name, session):
        raise HTTPException(status_code=400, detail=f"Username '{user.user_name}' already exists.")
    
    pwsd_hash = utils.get_password_hash(user.password)
    user.password = pwsd_hash
    db_user = User.model_validate(user)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user 

@router.post('/login', status_code=status.HTTP_202_ACCEPTED)
def user_login(form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):    
    user: Union[User,bool] = authenticate_user(
        session, form_data.username, form_data.password
    )
    
    if not user:
        raise HTTPException(status_code=400, 
            detail=f"Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_data = {
        "id": user.id,
        "user": user.user_name,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }
    access_token = utils.create_access_token(user_data)
    return {"access_token": access_token, "token_type": "bearer", "user_data":user_data}

@router.get('/users', response_model=List[UserPublic])
def user_list(  
    session: session_dep,
    user: User= Depends(get_current_user)
):
    try:
        user_list = list_users(session, user)
        return user_list
    except:
        raise HTTPException(status_code=500, detail="Failed to fetch users.")



    
@router.post('/logout')
def user_logout(username: str, session: session_dep):
    pass







