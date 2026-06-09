from __future__ import annotations
from typing import Any, List, Optional, Tuple, Dict
from enum import Enum

from msgspec import Struct, convert, json
from .user import User, extractVal

__all__ = ["Thread", "ThreadType", "ThreadFolder"]

class ThreadType(Enum):
    """Messenger Chat Thread Type"""
    USER = 1
    GROUP = 2
    PAGE = 3
    COMMUNITY = 2
    UNKNOWN = 3


class ThreadFolder(Enum):
    """Folder Location"""
    INBOX = "INBOX"
    ARCHIVE = "ARCHIVE"
    PENDING = "PENDING"
    SPAM = "SPAM"
    COMMUNITY = "COMMUNITY"
    E2EE ="E2EE_CUTOVER"
    OTHER = "OTHER"

class Thread(Struct, frozen=True, eq=False):
    """A Thread could be either User, Group, Community"""
    name: str
    """The name of the `Thread`"""
    thread_id: str
    """The `Thread`s Id"""
    message_count: int
    """Total messages sent to the `Thread`"""
    image: Optional[str]
    """`Thread` Cover photo"""
    thread_type: ThreadType
    """Type of the `Thread` (User, Group, Page e.g.)"""
    folder: ThreadFolder
    """The `Thread` folder's location (Inbox, Archaive e.g.)"""
    participants_nickname: Optional[Dict[str, str]]
    """A dict containing `Thread` participant's user Id as key and nickname as value."""
    thread_admins: Tuple[str]
    """A tuple of `Thread` admins Id"""
    privacy_mode: int
    """`Thread` Privacy"""
    approval_mode: int
    """`Thread`'s approval mode. when value is `1` approval mode is on  else off"""
    group_approval_queue: Tuple[Dict]
    """A tuple of dict containing the id of the requested and inviter users id."""
    joinable_mode: int
    """Wether join through Link is enabled in `Thread`"""
    joinable_link: Optional[str]
    """Invite link of the `Thread` to join."""
    is_joined: bool
    """Wether the Client is a participant of the `Thread`."""
    is_pinned: bool
    """True if the `Thread` has a message pinned."""
    all_participants: Tuple[User]
    """A Tuple of `User` object contains `Thread` participant's information."""
    description: Optional[str]
    """`Thread`'s description"""
    thread_theme: Optional[Dict]
    """`Thread`'s theme data"""
    pinned_messages: Optional[List] = None
    """Pinned messages Id in the Thread"""


def parse_thread_info(data: List[Dict])->Tuple[Thread, ...]:
    return tuple(get_and_parse(t) for t in data if t)

def get_and_parse(t)-> Thread:
    if "message_thread" in t:
        t = t["message_thread"]

    return Thread(
            name=t["name"],
            thread_id=t["thread_key"]["thread_fbid"] or t["thread_key"]["other_user_id"],
            thread_type=getThreadType.get(t["thread_type"], ThreadType.UNKNOWN),
            message_count=t["messages_count"],
            image=t["image"]["uri"] if t["image"] else None,
            folder=ThreadFolder(t["folder"]),
            approval_mode=t["approval_mode"],
            group_approval_queue=merge_join_request(t["group_approval_queue"]["nodes"]),
            joinable_mode=int(t["joinable_mode"]["mode"]),
            joinable_link=t["joinable_mode"]["link"],
            participants_nickname=merge_nickname(t["customization_info"]),
            thread_theme=t["thread_theme"],
            thread_admins=merge_admins(t["thread_admins"]),
            privacy_mode=t["privacy_mode"],
            is_joined=t["is_viewer_subscribed"],
            is_pinned=t["is_pinned"],
            pinned_messages=t["pinned_messages"] if "pinned_messages" in t else None,
            description=t["description"],
            all_participants=tuple(convert(nodes["node"]["messaging_actor"], type=User, dec_hook=extractVal) for nodes in t["all_participants"]["edges"]) if t["thread_type"] != "ONE_TO_ONE" else tuple() #type: ignore
            ) 



getThreadType = {
        "GROUP": ThreadType.GROUP,
        "ONE_TO_ONE": ThreadType.USER,
        "PAGE": ThreadType.PAGE,
        "COMMUNITY": ThreadType.COMMUNITY
        }

def merge_nickname(data: Dict)->Dict[str, str] | None:    
    return {dic["participant_id"]: dic["nickname"] for dic in data["participant_customizations"]} if data else None

def merge_admins(data)->Tuple[str]:
    return tuple(x["id"] for x in data) if data != [] else tuple()

def merge_join_request(data)-> Tuple:
    return tuple(
            {
                "requester": dic["requester"]["id"],
                "inviter": dic["inviter"]["id"],
                "request_timestamp": dic["request_timestamp"]
                } 
            for dic in data
            ) if data != [] else tuple()

