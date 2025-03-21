"""User management endpoints and functionality.

This module provides REST API endpoints for user management operations
including creation, retrieval, updating, and deletion of user resources.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from pydantic import BaseModel, EmailStr, Field, validator

router = APIRouter(prefix="/users", tags=["users"])


class UserBase(BaseModel):
    """Base user model with common attributes.

    This model serves as the foundation for user-related data schemas.
    """

    username: str = Field(
        ...,
        description="Unique username for the user",
        min_length=3,
        max_length=50,
        example="johndoe"
    )
    email: EmailStr = Field(
        ...,
        description="Email address of the user",
        example="john.doe@example.com"
    )
    full_name: Optional[str] = Field(
        None,
        description="Full name of the user",
        max_length=100,
        example="John Doe"
    )
    is_active: bool = Field(
        True,
        description="Whether the user account is active"
    )


class UserCreate(UserBase):
    """User creation model with password field."""

    password: str = Field(
        ...,
        description="User's password (will be hashed)",
        min_length=8,
        example="securepassword123"
    )

    @validator("password")
    def password_complexity(cls, v: str) -> str:
        """Validate password complexity requirements.

        Args:
            v: The password string to validate

        Returns:
            The validated password

        Raises:
            ValueError: If password doesn't meet complexity requirements
        """
        # Add your password validation logic here
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        # Example: Check for at least one number
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one number")
        return v


class User(UserBase):
    """User model returned from API endpoints.

    This model extends UserBase and adds user ID.
    """

    id: int = Field(..., description="Unique identifier for the user")

    class Config:
        """Pydantic model configuration."""

        schema_extra = {
            "example": {
                "id": 1,
                "username": "johndoe",
                "email": "john.doe@example.com",
                "full_name": "John Doe",
                "is_active": True
            }
        }


@router.post(
    "/",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    response_description="The created user"
)
async def create_user(
    user: UserCreate = Field(..., description="User information for creation")
) -> User:
    """Create a new user account.

    This endpoint registers a new user in the system with the provided details.
    The password will be securely hashed before storage.

    Args:
        user: User creation data including username, email, and password

    Returns:
        The created user object with generated ID

    Raises:
        HTTPException: If username or email already exists
    """
    # This would be replaced with actual database logic
    # Simulate a created user with ID for demonstration
    created_user = User(
        id=1,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active
    )
    return created_user


@router.get(
    "/",
    response_model=List[User],
    summary="List all users",
    response_description="List of users"
)
async def list_users(
    skip: int = Query(
        0,
        description="Number of users to skip for pagination",
        ge=0
    ),
    limit: int = Query(
        100,
        description="Maximum number of users to return",
        ge=1,
        le=100
    ),
    active_only: bool = Query(
        False,
        description="Filter only active users"
    )
) -> List[User]:
    """Retrieve a list of users.

    This endpoint returns a paginated list of users that can be filtered
    by active status.

    Args:
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return
        active_only: If true, only returns active users

    Returns:
        List of user objects
    """
    # This would be replaced with actual database query
    # Simulate a list of users for demonstration
    users = [
        User(
            id=1,
            username="johndoe",
            email="john.doe@example.com",
            full_name="John Doe",
            is_active=True
        ),
        User(
            id=2,
            username="janedoe",
            email="jane.doe@example.com",
            full_name="Jane Doe",
            is_active=True
        )
    ]

    if active_only:
        users = [user for user in users if user.is_active]

    return users[skip:skip+limit]


@router.get(
    "/{user_id}",
    response_model=User,
    summary="Get a specific user by ID",
    response_description="The requested user"
)
async def get_user(
    user_id: int = Path(
        ...,
        description="The ID of the user to retrieve",
        ge=1
    )
) -> User:
    """Retrieve a specific user by ID.

    Args:
        user_id: Unique identifier of the user to retrieve

    Returns:
        The user object if found

    Raises:
        HTTPException: If user is not found
    """
    # This would be replaced with actual database query
    # Simulate user retrieval for demonstration
    if user_id != 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )

    return User(
        id=1,
        username="johndoe",
        email="john.doe@example.com",
        full_name="John Doe",
        is_active=True
    )
