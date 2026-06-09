from __future__ import annotations

from msgspec import field, Struct
from typing import List


class Presence(Struct, frozen=True, eq=False):
    """Presence update of Users in inbox"""
    list_type: str
    """The type of presence_list recevied could be 'full' or 'inc' for half. 'full' Presence list only recevied on first listen or after reconnection."""
    presence_list: List[UserStatus] = field(name="list")
    """List of `UserStatus` contains user Presence status information."""

class UserStatus(Struct, frozen=True, eq=False):
    """A User's Presence information."""
    userId: int = field(name="u")
    """User id of the User"""
    isActive: int = field(name="p") # if 0 < isActive: user is online
    """If the value is greater than 0 then the `User` is active. Otherwise, `User` is offline."""
    lastActive: int = field(name="l", default=0)
    """Last Active timestamp of the `User`"""


