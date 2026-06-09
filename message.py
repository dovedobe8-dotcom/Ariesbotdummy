from __future__ import annotations

from enum import Enum
from msgspec import Struct, field
from typing import List, Optional

from .deltas.custom_type import Value
from .attachment import Attachment
from .thread import ThreadType, ThreadFolder




class MessageType(Enum):
    """Types of messages that can be received."""
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    GIF = "animated_image"  # GIFs
    EMOJI = "emoji"
    STICKER = "sticker"
    FILE = "file"
    LOCATION = "location"
    FACEBOOK_POST = "post"
    FACEBOOK_PROFILE = "profile"
    FACEBOOK_REEL = "reel"
    FACEBOOK_PRODUCT = "product"
    FACEBOOK_STORY = "story"
    FACEBOOK_GAME = "game"
    EXTERNAL_URL = "external_url"

    POLL_CREATED = "poll_created"
    POLL_VOTED = "poll_voted"
    MESSAGE_PINNED = "message_pinned"
    MESSAGE_UNSENT = "message_unsent"
    MESSAGE_REPLY = "message_reply"
    MESSAGE_REACTION = "message_reaction"
    ADMIN_TEXT = "admin_text"

class EmojiSize(Enum):
    """Size of emojis sent in messages."""
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"

class Reaction(Enum):
    """Represents Reaction states either ADDED or REMOVED"""
    ADDED = 0
    REMOVED = 1

class Mention(Struct, frozen=True, eq=False):
    """Represents a `User` mention in a message."""
    user_id: str = field(name="i")
    """The id of the user to mention"""
    offset: int = field(name="o")
    """The index in the text message where the mention starts"""
    length: int = field(name="l")
    """length of user name"""
    name: Optional[str] = None
    """User's name"""
    

class Mentions(Struct, frozen=True):
    """mention one or multiple users"""
    users: Optional[List[Mention]] = None

    def _to_payload(self) -> dict:
        if not self.users:
            return {}
        ids = [m.user_id for m in self.users]
        offsets = [str(m.offset) for m in self.users]
        lengths = [str(m.length) for m in self.users]
        types = ["p"] * len(self.users)
        return {
            "mention_ids": ",".join(ids),
            "mention_offsets": ",".join(offsets),
            "mention_lengths": ",".join(lengths),
            "mention_types": ",".join(types),
        }

    @classmethod
    def from_text(cls, text: str, users: List[tuple]) -> Mentions:
        mentions = []
        for user_id, name in users:
            offset = text.find(name)
            if offset == -1:
                raise ValueError(f"Name '{name}' not found in text")
            mentions.append(Mention(user_id=user_id, name=name, offset=offset, length=len(name)))
        return cls(mentions)




class MessageReaction(Struct, frozen=True, eq=False):
    """Represents A Reaction Message"""
    id: str = field(name="messageId")
    """The message Id"""
    thread_id: Value = field(name="threadKey")
    """The Thread Id of the message."""
    reactor: int = field(name="userId")
    """The `User` who reacted to the `Message`"""
    reacted_message_sender: int = field(name="senderId")
    """The Author of the message `User` reactor to."""
    reaction_type: Reaction = field(name="action")# 0 for adding 1 for removing
    """Type of the Reaction"""
    reaction: Optional[str] = None
    """The Reaction Emoji"""
    timestamp: Optional[int] = field(name="reactionTimestamp", default=None)
    """The timestamp of the Stamp"""

class MessageRemove(Struct, frozen=True, eq=False):
    """Client's removed message for himself"""
    ids: List[str] = field(name="messageIds")
    """List of the deleted `Message`'s Ids."""
    thread_id: Value = field(name="threadKey")
    """The Thread Id where the message belongs."""

class MessageUnsend(Struct, frozen=True, eq=False):
    """Unsent Message information."""
    id: str = field(name="messageID")
    """Message Id"""
    thread_id: Value = field(name="threadKey")
    """The Thread Id of the Message"""
    sender_id: int = field(name="senderID")
    """The User who unsent the messages"""
    timestamp: int = field(name="deletionTimestamp")
    """timestamp of the messages    """

class Message(Struct, frozen=True, eq=False):
    """Represents a facebook messenger message"""
    id: str
    """Id of the message"""
    text: str
    """The text of the message"""
    sender_id: str
    """The message sender's User id"""
    thread_id: str
    """The thread message was sent to."""
    thread_type: ThreadType
    """Type of the thread thread message was sent (User, Group, Page e.g.)"""
    reaction: Optional[List[MessageReaction]]
    """Id of the reactors"""
    message_type: MessageType 
    """Type of message (Video, Image, Text, e.g.)"""
    mentions: Optional[List[Mention]]
    """if any users were mentioned"""
    thread_folder: ThreadFolder
    """The Thread location INBOX, ARCHIVE etc."""
    thread_participants: Optional[tuple[int]]
    """Users in the thread message was sent."""
    attachments: Optional[List[Attachment]]
    """List of attachments data that were sent such as Image, Video, Shared Facebook Post/ youtube videos etc."""
    timestamp: int
    """The timestamp message was sent."""
    can_unsend: bool
    """Wether the the message can be unsent by client"""
    unsent: bool
    """wether the message is unsent for everyone"""
    replied_to_message: Optional[Message] = None
    """If this message was a reply to another message"""
    replied_to_message_id: Optional[str] = None


