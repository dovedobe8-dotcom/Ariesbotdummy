"""Commonly received json object in message data"""

from msgspec import Struct, field
from .deltas.custom_type import Value

class MessageData(Struct, frozen=True, omit_defaults=True):
    """A message metadata information, including message senderId (The User that triggered the eevnt), thread folder, message id, timestamp etc."""

    id: str = field(name="messageId")
    """Id of the message"""
    sender_id: str | int = field(name="actorFbId")
    """The user Who sent the message or triggered it"""
    folder: Value = field(name="folderId")
    """The Thread folder location such as Inbox, Archive etc. Usually It is `Inbox`"""
    timestamp: str | int 
    """The timestamp of the message."""
    thread_id: Value = field(name="threadKey")
    """The thread Id where the message was sent"""
    adminText: str = ""
    """Only received when in a group any admin related actions are done such as Kicking , adding memebers, promoting to admin, approving Users to group etc. """
    unsendType: str = "unknown"
    """Wether the message can be unsent or not. Client can only unsent if the value is 'can_unsend'"""


