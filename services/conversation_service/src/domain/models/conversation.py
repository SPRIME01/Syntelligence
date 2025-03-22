"""Conversation domain model.

This module defines the Conversation entity for the conversation domain.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from .message import Message


@dataclass
class Conversation:
    """Conversation entity that represents a sequence of messages.

    A conversation is a container for messages exchanged between users and AI.
    It has metadata such as a title, timestamps, and references to participants.

    Attributes:
        id: Unique identifier for the conversation
        title: Human-readable title of the conversation
        created_at: Timestamp when the conversation was created
        updated_at: Timestamp when the conversation was last updated
        created_by: Reference to the user who created the conversation
        is_archived: Whether the conversation has been archived
        messages: List of messages in the conversation
    """

    title: str
    created_by: UUID
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    is_archived: bool = False
    messages: List[Message] = field(default_factory=list)

    def add_message(self, message: Message) -> None:
        """Add a message to the conversation.

        This method appends a new message to the conversation and updates
        the 'updated_at' timestamp.

        Args:
            message: The message to add to the conversation
        """
        self.messages.append(message)
        self.updated_at = datetime.utcnow()

    def update_title(self, new_title: str) -> None:
        """Update the title of the conversation.

        Args:
            new_title: The new title for the conversation

        Raises:
            ValueError: If the new title is empty or invalid
        """
        if not new_title or new_title.strip() == "":
            raise ValueError("Conversation title cannot be empty")

        self.title = new_title
        self.updated_at = datetime.utcnow()

    def archive(self) -> None:
        """Archive the conversation.

        This marks the conversation as archived and updates the 'updated_at' timestamp.
        """
        self.is_archived = True
        self.updated_at = datetime.utcnow()

    def unarchive(self) -> None:
        """Unarchive the conversation.

        This marks the conversation as not archived and updates the 'updated_at' timestamp.
        """
        self.is_archived = False
        self.updated_at = datetime.utcnow()

    def get_latest_messages(self, limit: int = 10) -> List[Message]:
        """Get the most recent messages in the conversation.

        Args:
            limit: Maximum number of messages to return

        Returns:
            A list of the most recent messages, up to the specified limit
        """
        return sorted(self.messages, key=lambda m: m.timestamp, reverse=True)[:limit]
