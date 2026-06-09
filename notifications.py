from typing import Union
from msgspec import Struct, field 




class friendRequestList(Struct, frozen=True, eq=False, tag="mobile_requests_count", tag_field="type"):
    """New friend request list update. When friend request list is updated"""
    friend_requests: int = field(name="num_unread")
    """current count of friend request"""
    new_friend_request: int = field(name="num_unseen")
    """New friend request count"""


class friendUpdated(Struct, frozen=True, eq=False, tag="jewel_requests_remove_old", tag_field="type"):
    """Removed User id from friend request list either could be because The User cancelled friend request or Client accepted/removed friend request."""
    from_user: int = field(name="from") 
    """Removed User from friend request list"""


class FriendRequestState(Struct, frozen=True, eq=False, tag="friending_state_change", tag_field="type"):
    """Either Friend request confirmed or removed or sent by user"""
    user_id: int = field(name="userid")
    """The action done on the user"""
    action: str
    """action can be 'confirm', 'reject' or 'send'"""


class PokeNotification(Struct, frozen=True, eq=False, tag="live_poke", tag_field="type"):
    """Poked user details"""
    user_poked: int =  field(name="poke_source")
    """The user that Poked Client"""
    poke_time: int
    """The timestamp of the Poke"""



class PageNotification(Struct, frozen=True, eq=False):
    """Page notifucation extra information"""
    sender_id: str = field(name="senderId")
    """The `User` who sent message to Client's `Page`"""
    page_id: str = field(name="pageId")
    """The Id of the Page"""
    page_name: str = field(name="pageName")
    """Page's name"""
    message_id: str = field(name="messageId")
    """The Id of the sent message"""
    title: str 
    """Title of the notifucation"""
    text: str = field(name="body")
    """Text of the notifucation. Usually the text message that was sent to Page."""
    sender_profile_pic: str = field(name="senderProfPicUrl")
    """The user's profile picture"""
    page_profile_pic: str = field(name="pageProfPicUrl")
    """The Page's profile picture"""




class friendRequestSeen(Struct, frozen=True, eq=False, tag="friend_requests_seen", tag_field="type"):
    pass


class NotificationSeen(Struct, frozen=True, eq=False, tag="notifications_seen", tag_field="type"):
    pass

class NavigationNotify(Struct, frozen=True, eq=False, tag="nav_update_counts", tag_field="type"):
    pass

class ConfirmedFriend(Struct, frozen=True, eq=False, tag="jewel_friending_notifs", tag_field="type"):
    pass


FacebookNotifications = Union[friendRequestList, friendUpdated, FriendRequestState, PokeNotification, friendRequestSeen, NotificationSeen,NavigationNotify, ConfirmedFriend]
