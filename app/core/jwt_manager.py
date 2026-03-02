import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from app.config import settings

class JWTManager:
    ALGORITHM = "HS256"

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=JWTManager.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def decode_token(token: str) -> Optional[Dict[str, Any]]:
        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[JWTManager.ALGORITHM])
            return decoded_token
        except jwt.ExpiredSignatureError:
            return None
        except jwt.PyJWTError:
            return None
