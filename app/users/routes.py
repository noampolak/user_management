import logging
from datetime import timedelta
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from security import ACCESS_TOKEN_EXPIRE_MINUTES, auth_user, authenticate_user, create_access_token, get_password_hash
from users.schemas import UserCreate, UserLogin, Token, User, UserUpdate
from dependencies import get_db
from sqlalchemy.orm import Session
from users.models import User as UserModel

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/register")
def register(user: UserCreate,db: Session = Depends(get_db)):
    logger.info(f"Attempting to register new user with email: {user.email}")
    # Check if user already exists
    existing_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if existing_user:
        logger.warning(f"Registration failed: Email already exists: {user.email}")
        raise HTTPException(status_code=400, detail="Email already registered.")
    logger.info(f"Hashing password for user: {user.email}")
    hashed_pw = get_password_hash(user.password)
    user = UserModel(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        hashed_password=hashed_pw,
        disabled=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    logger.info(f"Successfully registered new user with email: {user.email}")
    return {"message": "User registered successfully"}

@router.post("/login",
            response_model=Token,
            )
def login(userLoginData: UserLogin, db: Session = Depends(get_db)):
    logger.info(f"Login attempt for user: {userLoginData.email}")
    user = authenticate_user(db, userLoginData.email, userLoginData.password)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    logger.info(f"Successful login for user: {user.email}")
    return Token(access_token=access_token, token_type="bearer")


@router.patch(
    "/update",
    openapi_extra={"security": [{"BearerAuth": []}]},
    dependencies=[Depends(auth_user)],
)
def update(userUpdateData: UserUpdate, db: Session = Depends(get_db) , user: User = Depends(auth_user)):
    logger.info(f"Attempting to update user: {userUpdateData.email}")
    
    user = db.query(UserModel).filter_by(email=userUpdateData.email).first()
    if user:
        user.first_name = userUpdateData.first_name
        user.last_name = userUpdateData.last_name
        user.email = userUpdateData.email
        user.hashed_password = get_password_hash(userUpdateData.password)
        db.commit()
        logger.info(f"Successfully updated user: {userUpdateData.email}")
        return {"message": "User updated successfully"}
    else:
        logger.warning(f"Update failed: Invalid credentials for user: {userUpdateData.email}")
        return {"message": "Invalid credentials"}
    

@router.get("/users", response_model=List[User])
def get_users(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    return users
