from typing import Any, Dict, List, Optional
from msgspec import Struct, json

from fbchat_muqit.models.attachment import StickerAttachment
from fbchat_muqit.models.thread import ThreadFolder, getThreadType
from .attachments_deltas import Mercury, extensibleattachment, BlobAttachment
from .parser import MessageParser
from ..message import Message, MessageReaction, MessageType, Reaction
from .custom_type import Value



class VNodes(Struct, frozen=True, eq=False):
    nodes: List

class VThreadMessages(Struct, frozen=True, eq=False):
    messages: VNodes 
    thread_key: Value
    thread_type: str
class VMessageThread(Struct, frozen=True, eq=False):
    message_thread: VThreadMessages

class VMessageAttachment(Struct, frozen=True, eq=False): 
    extensible_attachment: Optional[extensibleattachment] = None
    sticker: Optional[StickerAttachment] = None
    blob_attachments: Optional[List[BlobAttachment]] = None

def extract_thread_id(typ, obj)-> str:
    return Value(obj["thread_fbid"]) or Value(obj["other_user_id"])

thread_message_decoder = json.Decoder(type=List[VMessageThread], strict=False, dec_hook=extract_thread_id)


def parse_thread_message(payload: bytes)-> List[Message]:
    thread_message = thread_message_decoder.decode(payload)[0]
    thread_id = str(thread_message.message_thread.thread_key)
    nodes: List[Dict[str, Any]] = thread_message.message_thread.messages.nodes 

    messages = [
            Message(
                id=m["message_id"], 
                text=m["message"]["text"],
                sender_id=m["message_sender"]["id"],
                thread_id=thread_id,
                thread_type=getThreadType[thread_message.message_thread.thread_type],
                message_type=MessageType.TEXT,
                timestamp=m["timestamp_precise"],
                can_unsend=True if m["message_unsendability_status"] == "can_unsend" else False, 
                unsent=False,
                reaction=[
                    MessageReaction(
                        id="", 
                        reaction=r["reaction"],
                        reactor=r["user"]["id"],
                        thread_id=Value(thread_id),
                        reaction_type=Reaction.ADDED,
                        reacted_message_sender=m["message_sender"]["id"],
                        timestamp=None,
                    )   
                    for r in m["message_reactions"]
                ],
                mentions=None,
                thread_folder=ThreadFolder.INBOX,
                thread_participants=None,
                attachments=[MessageParser().parse_attachment(Mercury(
                    blob_attachment=m["blob_attachments"],
                    sticker_attachment=m["sticker"],
                    extensible_attachment=m["extensible_attachment"]
                    ))]
                )
            for m in nodes
            ]
    return messages


