"""
Custom Types to trigger msgspec's decoder hook to parse and flatten deep nested json.
the subclasses are just used for triggering msgspec decoder hook so no changes are made here `Value` can be treated as normal string and DecodedPayloadType as normal `tuple` etc.
"""

class Value(str):
    """A subclass or str class, no changes. Custom type to trigger dec_hook to extract value from `dict` (json response)."""

class PostId(str):
    """For Extracting id of a facebook post"""

class GenieType(str):
    """Custom type to extract genie_message's value from `dict`"""

class DecodedPayloadType(tuple):
    """Triggered to decode raw `bytes` payload"""

class ReplyIdType(str):
    """Custom type to extract nested `dict` value"""

class PayloadAttachmentType(tuple):
    """"""
class MentionType(list):
    """"""
