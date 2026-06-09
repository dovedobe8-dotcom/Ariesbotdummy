"""
Messenger Group related Events
All Struct classes here are used for decoding raw payloads
"""
from typing import Union

from msgspec import Raw, Struct
from ..messagesData import MessageData
from ..thread_actions import (
        ApprovalMode, 
        ApprovalQueue, 
        JoinableMode,
        ParticipantsAdded,
        ParticipantLeft,
        AdminRemoved, 
        ThreadName,
        ThreadMuteSettings,
        ThreadAction,
        ThreadFolderMove,
        ThreadDelete,
        ForcedFetch,

        # Admin Texts type
        AdminAdded,
        ThreadMessagePin,
        ThreadMessageUnPin,
        ThreadMessageSharing,
        ThreadMagicWord,
        ThreadNickname,
        ThreadTheme,
        ThreadEmoji
        )

# all types of event recevied
AllAdminText = {
        "joinable_group_link_mode_change",
        "joinable_group_link_reset",
        "change_thread_nickname",
        "change_thread_theme",
        # "change_thread_approval_mode",
        "change_thread_admins",
        "change_thread_quick_reaction",
        "magic_words",
        "limit_sharing",
        "instant_game_dynamic_custom_update",
        "unpin_messages_v2",
        "pin_messages_v2",
        }



class AdminTextMessage(Struct, frozen=True, eq=False, tag="AdminTextMessage", tag_field="class"):
    """"""
    messageMetadata: MessageData
    type: str
    untypedData: Raw



MessengerGroupDeltas = Union[ApprovalQueue, ApprovalMode, ParticipantsAdded, ParticipantLeft, AdminRemoved, ThreadName, AdminTextMessage, JoinableMode, ThreadMuteSettings, ThreadAction, ThreadFolderMove, ThreadDelete, ForcedFetch]
