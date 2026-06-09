import re
from typing import List 
from enum import Enum
from msgspec import Struct, field 
from msgspec.json import Decoder

from fbchat_muqit.exception.errors import FBChatError

class Audience(Enum):
    PUBLIC = "EVERYONE"
    FRIENDS = "FRIENDS"
    ONLYME = "SELF"

class Privacy(Struct, frozen=True):
    specific_users: List[int] = field(name="allow", default_factory=list)
    """Only allowed users will see the post"""
    except_users: List[int] = field(name="deny", default_factory=list)
    """Except the denied users everyone will see the post"""
    base_state: Audience = Audience.FRIENDS
    """Audience State of the post Public, friends, only etc."""

privacyDecoder = Decoder(type=Privacy, strict=False)

class PrivacyRow(Struct, frozen=True, eq=False):
    id: str
    privacy_row_input: Privacy = Privacy()

def extract_privacy_data(resp: str):
    # Remove control characters that break regex scanning
    cleaned = re.sub(r"[\x00-\x1f\x7f]", "", resp)

    # Extract privacy_write_id
    privacy_write_id = re.search(r'"privacy_write_id"\s*:\s*"([^"]+)"', cleaned)
    if privacy_write_id:
        privacy_write_id = privacy_write_id.group(1)
    else:
        raise FBChatError("Failed to get `privacy_write_id` value. Couldn't set up audience.")

    # Extract the first privacy_row_input (valid JSON object)
    row_match = re.search(r'"privacy_row_input"\s*:\s*({[^{}]+})', cleaned)
    privacy_row_input = None
    if row_match:
        try:
            privacy_row_input = privacyDecoder.decode(row_match.group(1))
        except Exception as e:
            pass

    return PrivacyRow(privacy_write_id, privacy_row_input or Privacy())



# ================= X =============================

class PrivacyRowOverride(Struct, frozen=True, eq=False):
    selected_row_override: Privacy

class PrivacyScope(Struct, frozen=True, eq=False):
    scope: PrivacyRowOverride


class PrivacyNode(Struct, frozen=True, eq=False):
    node: PrivacyScope

class OverridenPrivacy(Struct, frozen=True, eq=False):
    data: PrivacyNode

# =================== x  ===================
class UploadedPicture(Struct, frozen=True, eq=False):
    photoID: str 
    imageSrc: str 
    width: int 
    height: int 


class PictureUploadResponse(Struct, frozen=True, eq=False):
    payload: UploadedPicture


# ================== x =====================

class StoryInfo(Struct, frozen=True, eq=False):
    id: str

class CreatedPost(Struct, frozen=True, eq=False):
    story_id: str | None
    story: StoryInfo | None = None
    post_id: str | int | None = None

class StoryCreate(Struct, frozen=True, eq=False):
    story_create: CreatedPost

class ResponsePostData(Struct, frozen=True, eq=False):
    data: StoryCreate
