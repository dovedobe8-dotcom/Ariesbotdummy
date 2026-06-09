# pyright: reportUnknownVariableType=false
# pyright: reportUnknownMemberType=false
from msgspec import Struct, json
from typing import Any, Optional



class MessageSearchResult(Struct, frozen=True, eq=False):
    query: str
    """The Searched text"""
    result_index: int
    """Index of the query text"""
    thread_id: str
    """Thread Id of the message"""
    sender_name: str
    """The sender of the message"""
    message_id: str
    """Id of the message where query text was found."""
    timestamp_ms: int
    """timestamp of the message"""
    snippet: str
    """The message's text"""
    profile_pic_url: str 
    """message sender profile picture."""
    highlight_offset: str
    """offset of the query text in the message"""
    highlight_length: str
    """length of the highlighted query text in the message"""

class MessageSearchStatus(Struct, frozen=True, eq=False):
    query: str
    """query text"""
    total_results: int
    """total results found"""
    status: int
    """status of search result"""
    has_more: bool
    """If more messages has the query text or not"""
    next_cursor: Optional[str]
    """next message count probably not sure"""
    thread_id: str
    """Thread Id where query text was Searched"""

def parse_message_search(data: str):
    """Parse message search response from Facebook Messenger."""
    inner = json.decode(data)
    results = []
    status = None

    def decode_value(v)-> Any:
        """Decode Facebook's encoded values."""
        if isinstance(v, list) and len(v) >= 2 and isinstance(v[0], int):
            if v[0] == 19:  # String type
                return v[1]
            if v[0] == 9:   # Null type
                return None
        return v

    def walk(node):
        nonlocal status
        
        # Check if this is an operation node: [5, "operationName", ...args]
        if isinstance(node, list) and len(node) >= 2:
            if node[0] == 5 and isinstance(node[1], str):
                op = node[1]
                args = [decode_value(x) for x in node[2:]]
                
                if op == "insertMessageSearchResult":
                    # Based on the structure:
                    # [5, "insertMessageSearchResult", 
                    #   0:query, 1:index, 2:thread_id, 3:?, 4:?, 
                    #   5:sender_name, 6:message_id, 7:timestamp, 
                    #   8:snippet, 9:profile_pic_url, 10:?,
                    #   11:highlight_offset, 12:highlight_length, 13:?]
                    
                    if len(args) >= 13:
                        results.append(MessageSearchResult(
                            query=args[0] or "",
                            result_index=int(args[1]) if args[1] is not None else 0,
                            thread_id=args[2] or "",
                            sender_name=args[5] or "",
                            message_id=args[6] or "",
                            timestamp_ms=int(args[7]) if args[7] else 0,
                            snippet=args[8] or "",
                            profile_pic_url=args[9] or "",
                            highlight_offset=args[11] or "",
                            highlight_length=args[12] or ""
                        ))
                
                elif op == "updateMessageSearchQueryStatus":
                    # [5, "updateMessageSearchQueryStatus",
                    #   0:query, 1:total_results, 2:status, 3:has_more, 4:next_cursor, 5:thread_id, 6:?]
                    if len(args) >= 6:
                        status = MessageSearchStatus(
                            query=args[0] or "",
                            total_results=int(args[1]) if args[1] is not None else 0,
                            status=int(args[2]) if args[2] is not None else 0,
                            has_more=bool(args[3]) if args[3] is not None else False,
                            next_cursor=args[4],
                            thread_id=args[5] or ""
                        )
            # Recursively walk all list elements
            for item in node:
                if isinstance(item, (list, dict)):
                    walk(item)
        
        elif isinstance(node, dict):
            # Also walk dictionary values
            for value in node.values():
                if isinstance(value, (list, dict)):
                    walk(value)

    # Start walking from the root
    walk(inner)
    
    return {"results": results, "status": status}
