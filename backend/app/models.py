"""Data models for the Syntelligence application.

This module contains Pydantic models that represent the core domain entities
used throughout the application. These models handle data validation, serialization,
and provide clear type annotations.
"""

from datetime import datetime
from typing import Dict, List, Optional, Union
from pydantic import BaseModel, EmailStr, Field, validator


class UserProfile(BaseModel):
    """User profile information.

    Contains additional profile information about a user beyond
    the basic authentication details.

    Attributes:
        bio: A short biography or description provided by the user
        profile_image_url: URL to the user's profile image
        location: User's geographical location
        website: User's personal or professional website
        social_links: Dictionary of social media platform names to profile URLs
    """

    bio: Optional[str] = Field(
        None,
        description="Short biography or description",
        max_length=500
    )
    profile_image_url: Optional[str] = Field(
        None,
        description="URL to the user's profile image"
    )
    location: Optional[str] = Field(
        None,
        description="User's geographical location",
        max_length=100
    )
    website: Optional[str] = Field(
        None,
        description="User's personal or professional website"
    )
    social_links: Dict[str, str] = Field(
        default_factory=dict,
        description="Dictionary of social media platform names to profile URLs"
    )


class ProjectStatus(str):
    """Project status enumeration."""

    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class Project(BaseModel):
    """Project model representing a user-created project.

    This model contains all the information related to a project within
    the Syntelligence platform.

    Attributes:
        id: Unique identifier for the project
        title: The project title
        description: Detailed description of the project
        owner_id: ID of the user who owns the project
        collaborator_ids: List of user IDs who are collaborators
        status: Current project status (draft, active, completed, archived)
        created_at: When the project was created
        updated_at: When the project was last updated
        tags: List of tags associated with the project
        is_public: Whether the project is publicly visible
    """

    id: Optional[int] = Field(
        None,
        description="Unique identifier for the project"
    )
    title: str = Field(
        ...,
        description="The project title",
        min_length=3,
        max_length=100
    )
    description: str = Field(
        ...,
        description="Detailed description of the project",
        min_length=10
    )
    owner_id: int = Field(
        ...,
        description="ID of the user who owns the project"
    )
    collaborator_ids: List[int] = Field(
        default_factory=list,
        description="List of user IDs who are collaborators"
    )
    status: str = Field(
        ProjectStatus.DRAFT,
        description="Current project status (draft, active, completed, archived)"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the project was created"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the project was last updated"
    )
    tags: List[str] = Field(
        default_factory=list,
        description="List of tags associated with the project"
    )
    is_public: bool = Field(
        False,
        description="Whether the project is publicly visible"
    )

    @validator("status")
    def validate_status(cls, v: str) -> str:
        """Validate that the status is one of the allowed values.

        Args:
            v: Status value to validate

        Returns:
            The validated status

        Raises:
            ValueError: If status is not one of the allowed values
        """
        allowed_statuses = [
            ProjectStatus.DRAFT,
            ProjectStatus.ACTIVE,
            ProjectStatus.COMPLETED,
            ProjectStatus.ARCHIVED
        ]
        if v not in allowed_statuses:
            raise ValueError(
                f"Status must be one of: {', '.join(allowed_statuses)}"
            )
        return v

    @validator("updated_at")
    def updated_at_must_be_after_created_at(cls, v: datetime, values: Dict) -> datetime:
        """Ensure updated_at is not before created_at.

        Args:
            v: The updated_at value
            values: Dictionary of previously validated values

        Returns:
            The validated updated_at datetime

        Raises:
            ValueError: If updated_at is before created_at
        """
        if "created_at" in values and v < values["created_at"]:
            raise ValueError("updated_at cannot be before created_at")
        return v

    class Config:
        """Pydantic model configuration."""

        schema_extra = {
            "example": {
                "id": 1,
                "title": "AI Research Project",
                "description": "A research project investigating the latest advancements in AI technology.",
                "owner_id": 42,
                "collaborator_ids": [43, 44],
                "status": "active",
                "created_at": "2023-01-15T08:30:00",
                "updated_at": "2023-01-20T14:25:30",
                "tags": ["AI", "research", "machine-learning"],
                "is_public": True
            }
        }
