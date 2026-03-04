from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional, Dict, Any
from app.core.jwt_manager import JWTManager

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

def get_current_user_token(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = JWTManager.decode_token(token)
    if payload is None:
        raise credentials_exception
    
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception
        
    return payload

# Note: get_current_user implementation will require database dependency injection
def get_current_user_id(payload: Dict[str, Any] = Depends(get_current_user_token)) -> str:
    return payload.get("sub")

def require_role(allowed_roles: list[str]):
    def role_checker(payload: Dict[str, Any] = Depends(get_current_user_token)):
        user_role = payload.get("role")
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted"
            )
        return payload
    return role_checker
