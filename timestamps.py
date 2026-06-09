from typing import List, Optional, Union
from msgspec import Struct, field

from .deltas.custom_type import Value

class ReadReceipt(Struct, frozen=True, eq=False, tag="ReadReceipt", tag_field="class"):
    """When a `User` seen messages in a thread."""
    timestamp: str = field(name="actionTimestampMs")
    """timestamp of the message"""
    watermark_timestamp: str = field(name="watermarkTimestampMs")
    """seen timestamp"""
    user_id: str = field(name="actorFbId")
    """The user who seen the message"""
    folder: Value = field(name="folderId")
    """The Thread Folder where the user seen messages"""
    thread_id: Value = field(name="threadKey")
    """The Id of that Thread."""

class DeliveryReceipt(Struct, frozen=True, eq=False, tag="DeliveryReceipt", tag_field="class"):
    """Client's Delivered message Delivery information"""
    timestamp: int = field(name="deliveredWatermarkTimestampMs")
    """Delivered timestamp"""
    message_id: List[str] = field(name="messageIds")
    """List of Delivered message Id"""
    thread_id: Value = field(name="threadKey")
    """The Thread Id where message was Delivered."""
    user_id: Value = field(name="actorFbId")
    """The sender of the message."""

class MarkFolderSeen(Struct, frozen=True, eq=False, tag="MarkFolderSeen", tag_field="class"):
    """Usually received when you open messenger :)"""
    folders: List[str]
    """Usually Inbox can be Archive, Spam"""
    timestamp: str
    """The seen timestamp"""

class MarkRead(Struct, frozen=True, eq=False, tag="MarkRead", tag_field="class"):
    """Client's seen message information."""
    timestamp: str = field(name="actionTimestamp")
    """The message timestamp"""
    thread_ids: List[Value] = field(name="threadKeys")
    """List of seen messages Thread Id"""
    watermark_timestamp: str = field(name="watermarkTimestamp")
    """The seen timestamp"""
    folder: Optional[Value] = field(name="folderId", default=None)
    """The Thread Folder where the event occurred such as Inbox, Spam, Archive"""

class MarkUnread(Struct, frozen=True, eq=False, tag="MarkUnread", tag_field="class"):
    """Client's Unread marking Thread related information."""
    timestamp: str = field(name="actionTimestamp")
    """The timestamp of the event"""
    thread_ids: List[Value] = field(name="threadKeys")
    """List of Unread marked Thread Ids."""
# Used for deltaWrapper

TimestampDeltas = Union[ReadReceipt, DeliveryReceipt, MarkFolderSeen, MarkRead, MarkUnread]
