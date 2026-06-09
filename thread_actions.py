from typing import Optional, List
from msgspec import Struct, field

from .messagesData import MessageData
from .deltas.custom_type import Value




class addedParticipant(Struct, frozen=True, eq=False):
    """Adeed participant's information."""
    name: str = field(name="fullName")
    """added participant's name"""
    user_id: str = field(name="userFbId")
    """added participant's user id"""
    last_unsubscribed: Optional[str] = field(name="lastUnsubscribeTimestampMs", default=None)
    """join timestamp"""


################ All main classes ##################

class ApprovalMode(Struct, frozen=True, eq=False, tag="ApprovalMode", tag_field="class"):
    """Thread's Updated Approval mode data."""
    mode: str
    """mode wether Approval Mode is on 'APPROVALS'(on) or OPEN' (off)"""
    messageMetadata: MessageData 
    """Extra information about the message."""


class ApprovalQueue(Struct, frozen=True, eq=False, tag="ApprovalQueue", tag_field="class"):
    """A user's join request or disapproved join request's data exclude."""
    requester_id: str = field(name="recipientFbId")
    """Requested `User`'s user id"""
    action: str 
    """action can be either 'REQUESTED' or 'REMOVED'."""
    messageMetadata: MessageData
    """Extra message information inluding message author, timestamp, stamp"""
    inviter_id: Optional[str] = field(name="inviterFbId", default=None)
    """The participant who added another User to the group."""
    request_timestamp: Optional[str] = field(name="requestTimestamp", default=None)
    """Request timestamp"""
    requestSource: str = "JOIN_THROUGH_LINK"
    """Wether joined through Link (default value) or Added by another group participant if added then value will be 'ADD'"""


class JoinableMode(Struct, frozen=True, eq=False, tag="JoinableMode", tag_field="class"):
    """Joining through Link to a Group."""
    mode: str   # JOINABLE / PRIVATE
    """Can be joined through Link if value 'JOINABLE' and can't if value is 'PRIAVTE'"""
    messageMetadata: MessageData
    """Extra message information."""


class ParticipantsAdded(Struct, frozen=True, eq=False, tag="ParticipantsAddedToGroupThread", tag_field="class"):
    """Added Participant's information"""
    added_participants: List[addedParticipant] = field(name="addedParticipants")
    """List of 'addedParticipant' object contains added participants data."""
    messageMetadata: MessageData
    """Extra information such as author (The one who added the Users), timestamp etc."""
    participants: tuple = tuple()
    """Tuple of all participants Id in the Group."""

class ParticipantLeft(Struct, frozen=True, eq=False, tag="ParticipantLeftGroupThread", tag_field="class"):
    """Left participant's information"""
    left_participant: str = field(name="leftParticipantFbId")
    """The Id of the left participant."""
    messageMetadata: MessageData
    """Extra message information."""
    participants: tuple = tuple()
    """Tuple of all participants Id in the Group."""

class AdminRemoved(Struct, frozen=True, eq=False, tag="AdminRemovedFromGroupThread", tag_field="class"):
    """Removed Admin event related data."""
    removed_admins: List[str] = field(name="removedAdminFbIds")
    """List of removed admins ids"""
    messageMetadata: MessageData
    """The message metadata information"""

class ThreadName(Struct, frozen=True, eq=False, tag="ThreadName", tag_field="class"):
    """Updated Thread's name"""
    name: str
    """New name of the Thread"""
    messageMetadata: MessageData
    """Metadata of the message"""
    participants: tuple = tuple()
    """Tuple of all participants Id in the Group."""


# Payload class 
class ApprovedUser(Struct, frozen=True, eq=False):
    """Approved User event data"""
    thread_id: Value = field(name="threadKey")
    """The thread Id where the User was accepted."""
    contact_id: int = field(name="contactId")
    """The Admin Id who approved The User to Thread"""
    approved_user_id: int = field(name="subscribe_actor_id")
    """The approved User Id"""

# payload class
class ChangeViwerStatus(Struct, frozen=True, eq=False):
    """Changed Viewer Status information"""
    user_id: Value = field(name="actorFbid")
    """The User (Client) who changed the View"""
    thread_id: Value = field(name="threadKey")
    """The Thread's (User Thread) Id which view was changed"""
    can_reply: bool = field(name="canViewerReply")
    """User can reply to that Thread if `True` else it is `False`"""
    reason: int  # 0 for fb and 2 for messenger block
    """0 if the User blocked the Thread (User Thread in that case) in Facebook and 2 if in Messenger"""
    is_messenger_blocked: Optional[bool] = field(name="isMsgBlockedByViewer", default=None)
    """If User is blocked on Messenger"""
    messenger_blocked_timestamp: Optional[int] = field(name="isMsgBlockedTimestamp", default=None)
    """The block event timestamp"""
    is_facebook_blocked: Optional[bool] = field(name="isFBBlockedByViewer", default=None)
    """If the User is blocked in Facebook."""
    facebook_blocked_timestamp: Optional[int] = field(name="isFBBlockedTimestamp", default=None)
    """Facebook block timestamp"""


class MuteThread(Struct, frozen=True, eq=False):
    """Thread Mute information"""
    thread_id: Value = field(name="threadKey")
    """Muted Thread's Id"""
    mute_until: int = field(name="muteUntil")
    """Mute duration"""


class ThreadMuteSettings(Struct, frozen=True, eq=False, tag="ThreadMuteSettings", tag_field="class"):
    """Thread mute related information."""
    user_id: str = field(name="actorFbId")
    """The User (Client because other's mute information is not recevied) who muted the Thread """
    thread_id: Value = field(name="threadKey")
    """The Threas that was muted"""
    expire_time: int = field(name="expireTime")
    """Mute expire time."""

class ThreadAction(Struct, frozen=True, eq=False, tag="ThreadAction", tag_field="class"):
    """information of the Archived from Inbox."""
    action: str
    """The action that was done"""
    thread_id: Value = field(name="threadKey")
    """The Thread action was done on."""


class ThreadFolderMove(Struct, frozen=True, eq=False, tag="ThreadFolder", tag_field="class"):
    """Moved Thread folder data."""
    user_id: str 
    """The user who moved the Thread"""
    folder: str 
    """To the folder Location it was moved such as Inbox, Archive, etc."""
    thread_id: Value = field(name="threadKey")
    """The Thread that was moved."""

class ThreadDelete(Struct, frozen=True, eq=False, tag="ThreadDelete", tag_field="class"):
    """Deleted Thread information."""
    user_id: str = field(name="actorFbId") 
    """The User who deleted the Thread."""
    thread_ids: List[Value] = field(name="threadKeys")
    """List of Threas Ids that were deleted."""






# ----------------- Only  Group Admins action Related Delta -------- #

class AdminAdded(Struct, frozen=True, eq=False):
    """
    Added admin's information. 
    """

    aded_admin: str = field(name="TARGET_ID")
    """Removed/Added admin Id"""
    thread_type: str = field(name="THREAD_CATEGORY")
    """Type of the thread"""
    # admin_event: str = field(name="ADMIN_EVENT")


class ThreadMessagePin(Struct, frozen=True, eq=False):
    """Pinned Message"""
    message_id: str = field(name="pinned_message_id")
    """The pinned message's id"""

class ThreadMessageUnPin(Struct, frozen=True, eq=False):
    """Unpinned message"""
    message_id: str =  field(name="pinned_message_id")
    """The Unpinned message's id"""

class ThreadMessageSharing(Struct, frozen=True, eq=False):
    """Threas Message Sharing Mode information"""
    mode: str = field(name="limit_sharing_type")
    """Message mode is on if value is 'enabled' and off if value is 'disabled'"""
    sender_name: str 
    """The User's name who changed Message Sharing mode"""
    sender_id: str 
    """The User's Id"""

class ThreadMagicWord(Struct, frozen=True, eq=False):
    """Updated Magic word information."""
    magic_word: str 
    """The name of the Magic Word"""
    theme_name: str 
    """theme_name of the Magic word"""
    emoji: str = field(name="emoji_effect")
    """The emoji used for the Magic word."""
    removed_magic_word_count: str 
    """0 if not removed any Magic Word otherwise greater than 0"""
    new_magic_word_count: str
    """0 if not added any Magic Word otherwise greater than 0"""

class ThreadNickname(Struct, frozen=True, eq=False):
    """Changed nickname information of a participant"""
    nickname: str 
    """The new nickname of the User"""
    participant_id: str
    """The changed nickname User Id."""

class ThreadTheme(Struct, frozen=True, eq=False):
    """Updated Threaf theme information"""
    theme_id: str 
    """Id of the theme"""
    theme_name: str = field(name="theme_name_with_subtitle")
    """Name of the Theme"""
    theme_emoji: str 
    """The Quick Reaction Emoji for the Theme"""
    theme_type: str
    """Type of the theme"""
    theme_color: str
    """The color of the theme."""
    gradient: str
    """The gradient color of the theme"""
    accessibility_label: str
    """The keyword usee to label the theme."""

class ThreadEmoji(Struct, frozen=True, eq=False):
    """Updated Threaf Emoji information"""
    emoji: str = field(name="thread_quick_reaction_emoji")
    """The new quick reaction emoji"""
    emoji_url: str = field(name="thread_quick_reaction_emoji_url")
    """The url of the emoji"""


#--------------- End ------------------- #



class ForcedFetch(Struct, frozen=True, eq=False, tag="ForcedFetch", tag_field="class"):
    """Usually recevied when messenger group cover photo changes or along with other deltas"""
    threadKey: Value
    messageId: Optional[str] = None
    """messageId only recevied Usually when a Thread (Group) Picture is changed"""
    type: str = "None"
