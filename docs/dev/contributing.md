# Contributing Guide

Thank you for your interest in contributing to Syntelligence! This guide will help you understand our development workflow, coding standards, and documentation requirements.

## Development Workflow

1. **Fork the repository** (if you're not a core team member)
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Implement your changes**
4. **Document your code** with proper docstrings and type hints
5. **Write tests** for your implementation
6. **Submit a pull request**

## Code Style Guidelines

### Python

- Follow PEP 8 and use strict typing
- Use `typing.Protocol` for interfaces instead of ABCs where possible
- Write docstrings in the Google style format
- Use Pydantic for data validation

Example:

```python
from typing import List, Optional, Protocol
from pydantic import BaseModel, Field


class UserRepository(Protocol):
    """Interface for user data access.

    This protocol defines the contract that any user repository
    implementation must follow.
    """

    async def get_by_id(self, user_id: str) -> Optional["User"]:
        """Retrieve a user by their unique identifier.

        Args:
            user_id: The unique identifier of the user

        Returns:
            The user if found, None otherwise
        """
        ...


class User(BaseModel):
    """User model representing an authenticated user in the system.

    Attributes:
        id: Unique identifier for the user
        username: The user's chosen username
        email: The user's email address
        is_active: Whether the user account is active
    """

    id: str = Field(..., description="Unique identifier for the user")
    username: str = Field(..., description="The user's chosen username")
    email: str = Field(..., description="The user's email address")
    is_active: bool = Field(default=True, description="Whether the user account is active")


def get_active_users(users: List[User]) -> List[User]:
    """Filter a list of users to return only the active ones.

    Args:
        users: A list of User objects to filter

    Returns:
        A list containing only the active users

    Example:
        ```python
        all_users = [user1, user2, user3]
        active_users = get_active_users(all_users)
        ```
    """
    return [user for user in users if user.is_active]
```

### TypeScript

- Use TypeScript's strict mode
- Define interfaces for all data structures
- Use functional components with hooks for React

## Documentation Requirements

### Code Docstrings

All modules, classes, and functions should have docstrings following the Google style format. Include:

- Description of the purpose
- Args/Parameters with types and descriptions
- Returns with type and description
- Raises (if applicable)
- Examples (when useful)

### Documentation Pages

When adding new features, update the relevant documentation pages. Create new pages if necessary.

### API Documentation

FastAPI automatically generates OpenAPI/Swagger documentation from your code. To make this documentation useful:

- Add detailed descriptions to your Pydantic models
- Use appropriate response_model and status_code in FastAPI endpoints
- Include detailed path and query parameter descriptions

## Pre-commit Hooks

We use pre-commit hooks to ensure code quality. Install and set up pre-commit:

```bash
pip install pre-commit
pre-commit install
```

This will automatically run the configured hooks on your changes when you commit.
