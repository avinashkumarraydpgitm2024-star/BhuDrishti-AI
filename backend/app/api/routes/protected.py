from fastapi import APIRouter, Depends

from backend.app.core.auth import require_roles
from backend.app.models.user import User


router = APIRouter(
    prefix="/protected",
    tags=["Protected"],
)


@router.get("/authority")
def authority_only(
    current_user: User = Depends(
        require_roles(
            "admin",
            "authority",
        )
    ),
):
    return {
        "message": "Authority access granted.",
        "user": current_user.email,
        "role": current_user.role.value,
    }