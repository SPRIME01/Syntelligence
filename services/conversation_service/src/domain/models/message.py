"""Message domain model.

This module defines the Message entity for the conversation domain.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Dict, Optional
from uuid import UUID, uuid4


class MessageType(Enum):
    """Enumeration of possible message types in a conversation.

    This enum defines the various sender types for messages within a conversation.

    Attributes:
        USER: Message sent by a human user
        AI: Message sent by an AI assistant
        SYSTEM: Message sent by the system (e.g., notifications, prompts)
    """

    USER = "user"
    AI = "ai"
    SYSTEM = "system"


@dataclass
class Message:
    """Message entity representing a single communication in a conversation.

    A message contains the content of the communication, metadata about
    who sent it and when, and its type (user, AI, or system).

    Attributes:
        id: Unique identifier for the message
        content: The actual text content of the message
        sender_id: Reference to the entity that sent the message
        message_type: Type of message (user, AI, or system)
        timestamp: When the message was created
        metadata: Additional context or data associated with the message
    """

    content: str
    sender_id: UUID
    message_type: MessageType
    conversation_id: UUID
    id: UUID = field(default_factory=uuid4)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict = field(default_factory=dict)

    @property
    def is_user_message(self) -> bool:
        """Check if the message was sent by a user.

        Returns:
            True if the message is from a user, False otherwise
        """
        return self.message_type == MessageType.USER

    @property
    def is_ai_message(self) -> bool:
        """Check if the message was sent by an AI.

        Returns:
            True if the message is from an AI, False otherwise
        """
        return self.message_type == MessageType.AI

    @property
    def is_system_message(self) -> bool:
        """Check if the message was sent by the system.

        Returns:
            True if the message is from the system, False otherwise
        """
        return self.message_type == MessageType.SYSTEM

    def update_content(self, new_content: str) -> None:
        """Update the content of the message.

        Args:
            new_content: The new content for the message

        Raises:
            ValueError: If the new content is empty or invalid
        """
        if not new_content or new_content.strip() == "":
            raise ValueError("Message content cannot be empty")

        self.content = new_content

    def add_metadata(self, key: str, value) -> None:
        """Add or update metadata for the message.

        Args:
            key: The metadata key
            value: The metadata value
        """
        self.metadata[key] = value
