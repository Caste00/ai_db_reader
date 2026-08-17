from fastapi import APIRouter, HTTPException, status

from schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from memory.crud import create_user, get_user_by_surname
from models.user import User
from auth.security import generate_jwt, generate_password_hash, check_password

router = APIRouter(prefix="/auth", tags=["auth"])

DEFAULT_ROLE = "user"

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest):
    if get_user_by_surname(data.username) is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already used")

    user = User(
        name=data.username,
        password_hash=generate_password_hash(data.password),
        role=DEFAULT_ROLE
    )
    user = create_user(user)

    token = generate_jwt(user.id, user.role)
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest):
    user = get_user_by_surname(data.username)

    if user is None or not check_password(user.password_hash, data.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not valid credentials")

    token = generate_jwt(user.id, user.role)
    return TokenResponse(access_token=token)