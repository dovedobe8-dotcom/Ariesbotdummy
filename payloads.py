"""
Received Payloads from "ClientPayload" json structure.
Struct classes are used to parse them into Class objects instead of parsing into dict using standard json module.
"""

from typing import Optional, List
from msgspec import Struct, field


from ..messagesData import MessageData
from .custom_type import MentionType, Value
from .attachments_deltas import PayloadAttachments 
from ..message import MessageReaction, MessageRemove, MessageUnsend
from ..notifications import PageNotification
from ..thread_actions import ChangeViwerStatus, ApprovedUser, MuteThread

class MagicWord(Struct, frozen=True, eq=False):
    magic_word: str = field(name="magicWord")
    timestamp: str = field(name="timestampMS")
    emoji: str

class PayloadReplyMessage(Struct, frozen=True, eq=False):
    """"""
    messageMetadata: MessageData 
    body: Optional[str] = None
    messageReply: Optional[Value] = None
    attachments: Optional[List[PayloadAttachments]] = None 
    mentions: MentionType  = field(name="data", default=MentionType())
    participants: tuple = tuple()


class PayloadDeltaReply(Struct, frozen=True, eq=False):
    """"""
    repliedToMessage: Optional[PayloadReplyMessage] = None # main message
    message: Optional[PayloadReplyMessage] = None   # the message `main` message replied to


class PayloadThreadTheme(Struct, frozen=True, eq=False):
    """"""
    # thread_id: Value = field(name="threadKey")
    # theme_id: int = field(name="themeId")
    # fallbackColor: str 
    # gradientColors: List[str]
    # background_image_id: Value = field(name="backgroundAsset")
    # backgroundGradientColors: List[str]
    # titleBarBackgroundColor: str
    # composerBackgroundColor: str
    # titleBarTextColor: str
    # titleBarAttributionColor: str
    # composerInputBackgroundColor: str 
    # composerInputPlaceholderColor: str
    # inboundMessageGradientColors: List[str]
    # titleBarButtonTintColor: str
    # composerTintColor: str
    # composerUnselectedTintColor: str
    # messageTextColor: str
    # inboundMessageTextColor: str
    # deliveryReceiptColor: str
    # tertiaryTextColor: str
    # primaryButtonBackgroundColor: str
    # voiceRecordSoundwaveColor: str
    # accessibility_label: str = field(name="accessibilityLabel")

class PayloadThreadEmoji(Struct, frozen=True, eq=False):
    """"""
    # thread_id: Value = field(name="threadKey")
    # emoji: str


class PayloadMagicWords(Struct, frozen=True, eq=False):
    """"""
    # thread_id: Value = field(name="threadKey")
    # newMagicWords: List[MagicWord]
    # removedMagicWords: List[str]


class PayloadAdminsAdded(Struct, frozen=True, eq=False):
    """"""
    # thread_id: Value = field(name="threadKey")
    # added_admins: List[Value] = field(name="promotedAdmins")

    
class PayloadMoveToArchive(Struct, frozen=True, eq=False):
    """"""

# class MessageUnsend moved to message.py for documentaion

# class MessageReaction moved to message.py 

# class MessageRemove moved to message.py

# class PageNotification moved to fbnotification.py

# class ChangeViwerStatus moved to thread_actions.py

# class ApprovedUser moved to thread_actions.py


class DeltaMessageReply(Struct, frozen=True):
    messageReply: Optional[PayloadDeltaReply] = field(name="deltaMessageReply", default=None)
    replyType: Optional[int] = None
    messageReaction: Optional[MessageReaction] = field(name="deltaMessageReaction", default=None)
    messageUnsend: Optional[MessageUnsend] = field(name="deltaRecallMessageData", default=None)
    messageRemove: Optional[MessageRemove] =  field(name="deltaRemoveMessage", default=None)

    UpdateThreadTheme: Optional[PayloadThreadTheme] = field(name="deltaUpdateThreadTheme", default=None)
    UpdateThreadEmoji: Optional[PayloadThreadEmoji] = field(name="deltaUpdateThreadEmoji", default=None)
    UpdateMagicWords: Optional[PayloadMagicWords] = field(name="deltaUpdateMagicWords", default=None)
    PromoteGroupThreadAdmin: Optional[PayloadAdminsAdded] = field(name="deltaPromoteGroupThreadAdmin", default=None)
    AcceptToGroupThread: Optional[ApprovedUser] = field(name="deltaAcceptGroupThread", default=None)
    muteThread: Optional[MuteThread] = field(name="deltaMuteCallsFromThread", default=None)
    moveThreadToArchive: Optional[PayloadMoveToArchive] = field(name="deltaUpdatePinnedThread", default=None)

    changeViewerStatus: Optional[ChangeViwerStatus] = field(name="deltaChangeViewerStatus", default=None)
    pageNotification: Optional[PageNotification] = field(name="deltaBiiMPageMessageNotification", default=None)

