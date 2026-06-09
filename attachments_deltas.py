"""
All attachment related delta classes
Only used to decode and Parse recived deltas from mqtt.


msgspec decoing:
Raw Mqtt response (Recive bytes) -> Delta classes (parse to class) -> Attachment class (parse again to proper attachment classes based on type Image, Video e.g.)
"""


from msgspec import Struct, field
from typing import Optional, List

from .custom_type import Value, GenieType, PayloadAttachmentType
from ..attachment import StickerAttachment, BlobAttachment, Media, TargetType



class storyattachment(Struct, eq=False, frozen=True):
    """unnecessary fields are not inlucded from json"""
    title: Value = field(name="title_with_entities")
    media: Optional[Media]
    url: Optional[str] = field(default_factory=str)
    target: TargetType = None
    description: Optional[Value] = None
    source: Optional[Value] = None
    subattachments: List = field(default_factory=list)

class extensibleattachment(Struct, eq=False, frozen=True):
    """"""
    legacy_attachment_id: str
    genie_attachment: GenieType
    story_attachment: storyattachment


class Mercury(Struct, frozen=True, eq=False): 
    extensible_attachment: Optional[extensibleattachment] = None
    sticker_attachment: Optional[StickerAttachment] = None
    blob_attachment: Optional[BlobAttachment] = None

class RawAttachments(Struct, frozen=True, omit_defaults=True):
    mercury: Mercury
    id: Optional[str] = None


class PayloadAttachments(Struct, frozen=True, eq=False):
    id: str
    mercuryJSON: PayloadAttachmentType  # usually recives a json string not dict i guess manual parsing needed here by using custom type 

"""--------------- End Delta Attachment types -------------------"""
