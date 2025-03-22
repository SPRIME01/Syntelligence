"""Conversation service interface.

This module defines the interface for conversation domain services
following the Domain-Driven Design (DDD) principles.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Protocol
from uuid import UUID

from ..models.conversation import Conversation
from ..models.message import Message


class ConversationServiceInterface(Protocol):
    """Interface for conversation domain services.

    This protocol defines the contract that any conversation service implementation
    must fulfill. It follows the port pattern from hexagonal/ports and adapters
    architecture.

    The conversation service is responsible for managing conversations and their
    messages, including creation, retrieval, and update operations.
    """

    async def create_conversation(self, title: str, user_id: UUID) -> Conversation:
        """Create a new conversation.

        Args:
            title: The title of the conversation
            user_id: The unique identifier of the user creating the conversation

        Returns:
            A new Conversation entity

        Raises:
            ValueError: If the title is empty or invalid
            PermissionError: If the user lacks permission to create conversations
        """
        ...

    async def get_conversation(self, conversation_id: UUID) -> Optional[Conversation]:
        """Retrieve a conversation by its ID.

        Args:
            conversation_id: The unique identifier of the conversation to retrieve

        Returns:
            The requested Conversation entity, or None if not found
        """
        ...

    async def update_conversation(self, conversation_id: UUID, title: Optional[str] = None) -> Conversation:
        """Update an existing conversation.

        Args:
            conversation_id: The unique identifier of the conversation to update
            title: The new title for the conversation (if provided)

        Returns:
            The updated Conversation entity

        Raises:
            ValueError: If the conversation does not exist
            PermissionError: If the user lacks permission to update the conversation
        """
        ...

    async def delete_conversation(self, conversation_id: UUID) -> bool:
        """Delete a conversation.

        Args:
            conversation_id: The unique identifier of the conversation to delete

        Returns:
            True if the conversation was successfully deleted, False otherwise

        Raises:
            PermissionError: If the user lacks permission to delete the conversation
        """
        ...

    async def add_message(self, conversation_id: UUID, content: str,
                         sender_id: UUID, message_type: str) -> Message:
        """Add a message to a conversation.

        Args:
            conversation_id: The unique identifier of the conversation
            content: The content of the message
            sender_id: The unique identifier of the message sender
            message_type: The type of message (e.g., 'user', 'system', 'ai')

        Returns:
            The newly created Message entity

        Raises:
            ValueError: If the conversation does not exist or content is invalid
            PermissionError: If the user lacks permission to add messages
        """
        ...

    async def get_messages(self, conversation_id: UUID,
                          limit: int = 50,
                          before_timestamp: Optional[float] = None) -> List[Message]:
        """Retrieve messages from a conversation.

        Args:
            conversation_id: The unique identifier of the conversation
            limit: Maximum number of messages to retrieve
            before_timestamp: If provided, only messages before this timestamp will be returned

        Returns:
            A list of Message entities belonging to the conversation

        Raises:
            ValueError: If the conversation does not exist
            PermissionError: If the user lacks permission to view the conversation
        """
        ...

    async def get_user_conversations(self, user_id: UUID,
                                   limit: int = 20,
                                   offset: int = 0) -> List[Conversation]:
        """Retrieve conversations associated with a user.

        Args:
            user_id: The unique identifier of the user
            limit: Maximum number of conversations to retrieve
            offset: Number of conversations to skip (for pagination)

        Returns:
            A list of Conversation entities associated with the user

        Raises:
            PermissionError: If the requester lacks permission to view the user's conversations
        """
        ...
