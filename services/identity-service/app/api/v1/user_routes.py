from fastapi import APIRouter, Depends
from typing import Dict, Any
from app.core.security import get_current_user_token, require_role
from app.constants import ROLES

router = APIRouter()

@router.get("/me")
async def read_users_me(current_user: Dict[str, Any] = Depends(get_current_user_token)):
    """
    Get current user profile based on JWT token.
    """
    return {"message": "User profile information will be retrieved here", "user_claims": current_user}

@router.get("/admin-only")
async def read_admin_data(current_user: Dict[str, Any] = Depends(require_role([ROLES["SUPER_ADMIN"]]))):
    """
    Example of an admin-only route.
    """
    return {"message": "Welcome Admin!"}
