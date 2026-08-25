from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.core.security import (
    create_access_token,
    create_refresh_token,
)
from backend.app.schemas.user import (
    RefreshTokenRequest,
    TokenResponse,
    UserCreate,
    UserLogin,
    UserRead,
)

from backend.app.services.user_service import (
    authenticate_user,
    create_user,
    get_user_by_email,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
) -> UserRead:
    existing_user = get_user_by_email(
        db,
        str(user_data.email),
    )

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )

    user = create_user(
        db=db,
        user_data=user_data,
    )

    return UserRead.model_validate(user)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login_user(
    login_data: UserLogin,
    db: Session = Depends(get_db),
) -> TokenResponse:
    user = authenticate_user(
        db=db,
        email=str(login_data.email),
        password=login_data.password,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    access_token = create_access_token(
        subject=user.public_id,
        extra_claims={
            "role": user.role.value,
        },
    )

    refresh_token = create_refresh_token(
        subject=user.public_id,
        extra_claims={
            "role": user.role.value,
        },
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )
from backend.app.core.auth import get_current_user
from backend.app.models.user import User


@router.get(
    "/me",
    response_model=UserRead,
)
def read_current_user(
    current_user: User = Depends(get_current_user),
) -> UserRead:
    return UserRead.model_validate(current_user)

@router.post(
    "/refresh",
    response_model=TokenResponse,
)
def refresh_access_token(
    token_data: RefreshTokenRequest,
) -> TokenResponse:
    from jwt import InvalidTokenError

    from backend.app.core.security import decode_token

    try:
        payload = decode_token(token_data.refresh_token)

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token.",
            )

        subject = payload.get("sub")
        role = payload.get("role")

        if not subject:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token.",
            )

    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token.",
        )

    new_access_token = create_access_token(
        subject=subject,
        extra_claims={
            "role": role,
        },
    )

    new_refresh_token = create_refresh_token(
        subject=subject,
        extra_claims={
            "role": role,
        },
    )

    return TokenResponse(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
    )