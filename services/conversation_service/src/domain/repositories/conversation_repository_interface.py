"""Conversation repository interface.

This module defines the interface for persistence operations on conversation entities.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Protocol
from uuid import UUID

from ..models.conversation import Conversation


class ConversationRepositoryInterface(Protocol):
    """Interface for conversation persistence operations.

    This protocol defines the contract that any conversation repository implementation
    must fulfill, following the repository pattern from Domain-Driven Design.

    The repository abstracts the persistence details and provides a collection-like
    interface for accessing domain entities.
    """

    async def save(self, conversation: Conversation) -> Conversation:
        """Save a conversation entity to the repository.

        Args:
            conversation: The conversation entity to save

        Returns:
            The saved conversation entity, potentially with updated fields

        Raises:
            RepositoryError: If there is an error saving the entity
        """
        ...

    async def get_by_id(self, conversation_id: UUID) -> Optional[Conversation]:
        """Retrieve a conversation by its unique identifier.

        Args:
            conversation_id: The unique identifier of the conversation

        Returns:
            The conversation entity if found, None otherwise

        Raises:
            RepositoryError: If there is an error retrieving the entity
        """
        ...

    async def get_by_user(self, user_id: UUID, limit: int = 20, offset: int = 0) -> List[Conversation]:
        """Retrieve conversations created by a specific user.

        Args:
            user_id: The unique identifier of the user
            limit: Maximum number of conversations to retrieve
            offset: Number of conversations to skip (for pagination)

        Returns:
            A list of conversation entities created by the user

        Raises:
            RepositoryError: If there is an error retrieving the entities
        """
        ...

    async def delete(self, conversation_id: UUID) -> bool:
        """Delete a conversation from the repository.

        Args:
            conversation_id: The unique identifier of the conversation to delete

        Returns:
            True if the conversation was successfully deleted, False otherwise

        Raises:
            RepositoryError: If there is an error deleting the entity
        """
        ...
