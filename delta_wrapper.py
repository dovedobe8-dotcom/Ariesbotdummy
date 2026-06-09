"""
Instead of dataclasses or attrs, msgspec's `Struct` classes are used to automatically decode and Parse received json payloads. 
"""

from __future__ import annotations



from typing import List, Optional, Union
from msgspec import Struct, field

from .custom_type import (
        DecodedPayloadType, 
        MentionType, 
    )

from .attachments_deltas import (
        RawAttachments,
        )

# Delta classss
from .group_deltas import MessengerGroupDeltas
from ..timestamps import TimestampDeltas

from ..messagesData import MessageData
from .payloads import DeltaMessageReply
from ..typing import Typing 
from ..presence import Presence


class ClientPayloadDelta(Struct, frozen=True, eq=False):
    """"""
    deltas: List[DeltaMessageReply]

class ClientPayload(Struct, frozen=True, eq=False, tag="ClientPayload", tag_field="class"):
    payload: DecodedPayloadType  # receives `ClientPayloadDelta` object


class NewMessageDelta(Struct, frozen=True, eq=False, tag="NewMessage", tag_field="class"):

    messageMetadata: MessageData
    body: Optional[str] = None
    attachments: List[RawAttachments] = list()
    mentions: MentionType = field(name="data", default=MentionType())
    participants: tuple = tuple()


class NoOpDelta(Struct, frozen=True, eq=False, tag="NoOp", tag_field="class"):
    """"""

DeltaTypes = Union[NewMessageDelta, ClientPayload, NoOpDelta, TimestampDeltas, MessengerGroupDeltas]

# ------------------ Main Parent Delta wrappers ------------------- #

class DeltaWrapper(Struct, frozen=True, eq=False):
    deltas: List[DeltaTypes]  # automatically parsed by msgspec based on tag
    firstDeltaSeqId: Optional[int] = None
    lastIssuedSeqId: Optional[int] = None
    syncToken: Optional[str] = None

# class Typing is Parent wrapper

# class Presence is Parent Wrapper 


class FirstFetch(Struct, frozen=True, eq=False):
    firstDeltaSeqId: int
    queueEntityId: int
    syncToken: str


# ------------------ End Delta wrappers ------------------- #

