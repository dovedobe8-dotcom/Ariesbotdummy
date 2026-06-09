from msgspec import Struct, field


class Typing(Struct, frozen=True, eq=False):
    """Typing information of the Typer"""
    sender_id: int = field(name="sender_fbid")
    """The Id of the User who is typing"""
    state: int
    """1 for typing status and 0 for not typing."""
    thread_id: str = field(name="thread", default="")
    """Thw thread Id where user is typing if it is empty then It is one-to-one so sender_id and thread_id is same."""
