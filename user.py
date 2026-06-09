from typing import Dict, Optional
from msgspec import Struct, json, field
from .deltas.custom_type import Value
from ..exception.errors import ParsingError

__all__ = ["User"]

GENDERS = {
    0: "unknown",
    1: "female",
    2: "male",
    3: "female",
    4: "male",
    5: "mixed",
    6: "neuter",
    7: "unknown",
    8: "female_plural",
    9: "male_plural",
    10: "neuter_plural",
    11: "unknown_plural",
    # For graphql requests
    "UNKNOWN": "unknown",
    "FEMALE": "female_singular",
    "MALE": "male_singular",
    "NEUTER": "neuter_singular",
}

class User(Struct, frozen=True, eq=False):
    """Represents a Facebook User."""
    id: str
    """Facebook `User`'s uid"""
    name: str
    """Facebook `User`'s name"""
    first_name: str = field(name="short_name", default="")
    "The first name of the `User`"
    username: str = ""
    """The username of the User"""
    gender: str = ""
    """Gender of the user."""
    url: Optional[str] = ""
    """Facebook profile url of the `User`"""
    is_friend: bool = field(name="is_viewer_friend", default=False)
    """Wether the Client account is friend with the `User`"""
    is_blocked: bool = field(name="is_message_blocked_by_viewer", default=False)
    """Wether the client blocked or blocked by the `User` """
    image: Optional[Value] = field(name="big_image_src", default=None)
    """The profile picture url of the `User`"""
    alternate_name: Optional[str] = None
    """The alternate name of the Facebook `User`"""

def extractVal(typ, obj):
    if typ is Value:
        if isinstance(obj, dict):
            return Value(next(iter(obj.values())))
        return Value()

def parse_user_graphql(payload) -> Dict[str, User]:
    """Parses GraphQL responses that includes User info (works with dict or bytes)."""
    if isinstance(payload, dict):
        json_data = payload
    else:
        json_data = json.decode(payload)

    users_dict = {}
    profiles = json_data["payload"].get("profiles", {})
    for k, v in profiles.items():
        users_dict[k] = _parse_user(k, v)
    return users_dict

def _parse_user(k, v) -> User:
    """Parse a single user from GraphQL response (handles new payload structure)."""
    try:
        user_id = v.get("id", k)
        url = v.get("uri", "")

        return User(
            id=user_id,
            name=v.get("name", ""),
            first_name=v.get("firstName", ""),
            username=v.get("vanity", ""),
            gender=GENDERS.get(v.get("gender", "UNKNOWN"), "unknown"),
            url=url,
            is_friend=v.get("is_friend", False),
            is_blocked=v.get("is_blocked", False),
            image=v.get("thumbSrc", None),
            alternate_name=v.get("alternateName", None)
        )
    except Exception as e:
        raise ParsingError(f"Failed to parse User ({k})", original_exception=e)
