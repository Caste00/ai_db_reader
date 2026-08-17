import bcrypt
import jwt
from datetime import datetime, timezone, timedelta
from utils.config import config

def generate_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode('utf-8')


def check_password(password_hash: str, password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))


def generate_jwt(user_id, role: str) -> str:
    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=config.auth.access_token_expire_minutes)
    }
    return jwt.encode(payload, config.auth.secred_key, algorithm="HS256")


def decode_jwt(token):
    try:
        return jwt.decode(token, config.auth.secred_key, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise InvalidTokenError("Expired token")
    except Exception as e:
        raise InvalidTokenError(f"Not valid token: {e}")

        
class InvalidTokenError(Exception):
    pass
