"""Conversation domain events.

This module defines domain events for the conversation domain following
the Domain-Driven Design (DDD) principles.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional
from uuid import UUID


@dataclass(frozen=True)
class ConversationEvent:
    """Base class for all conversation domain events.

    This is the base class that all conversation-related domain events should inherit from.
    It provides common attributes needed for event handling and processing.

    Attributes:
        event_id: Unique identifier for the event
        conversation_id: The ID of the conversation this event relates to
        timestamp: When the event occurred
        user_id: The ID of the user who triggered the event
    """

    event_id: UUID
    conversation_id: UUID
    timestamp: datetime
    user_id: UUID


@dataclass(frozen=True)
class ConversationCreated(ConversationEvent):
    """Event raised when a new conversation is created.

    This event is published when a user creates a new conversation in the system.

    Attributes:
        title: The title of the created conversation
    """

    title: str


@dataclass(frozen=True)
class ConversationTitleUpdated(ConversationEvent):
    """Event raised when a conversation's title is updated.

    This event is published when a conversation's title is changed.

    Attributes:
        new_title: The updated title of the conversation
        old_title: The previous title of the conversation
    """

    new_title: str
    old_title: str


@dataclass(frozen=True)
class ConversationArchived(ConversationEvent):
    """Event raised when a conversation is archived.

    This event is published when a user archives a conversation.
    """

    pass


@dataclass(frozen=True)
class ConversationUnarchived(ConversationEvent):
    """Event raised when a conversation is unarchived.

    This event is published when a user restores a previously archived conversation.
    """

    pass


@dataclass(frozen=True)
class ConversationDeleted(ConversationEvent):
    """Event raised when a conversation is deleted.

    This event is published when a user permanently deletes a conversation.
    """

    pass


@dataclass(frozen=True)
class MessageAdded(ConversationEvent):
    """Event raised when a message is added to a conversation.

    This event is published when a new message is added to an existing conversation.

    Attributes:
        message_id: The ID of the newly added message
        message_type: The type of message (user, ai, system)
        content: The content of the message
        metadata: Additional metadata associated with the message
    """

    message_id: UUID
    message_type: str
    content: str
    metadata: Dict = None
