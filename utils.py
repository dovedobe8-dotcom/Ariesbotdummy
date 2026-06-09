import time
import json
import uuid


from random import random
from typing import Dict, Optional, Any
from random import random


from ..exception.errors import (
        ValidationError
        )

def now() -> int:
    """Get current timestamp in milliseconds."""
    return int(time.time() * 1000)
    
def generate_uuid() -> str:
    """Generate uuid4 string"""
    return str(uuid.uuid4())

def generate_message_id(client_id: Optional[str] = None) -> str:
    """Generate a unique message ID."""
    k = now()
    l = int(random() * 4294967295)
    return f"<{k}:{l}-{client_id}@mail.projektitan.com>"
    

def generate_offline_threading_id() -> str:
    """Generate offline threading ID."""
    ret = now()
    value = int(random() * 4294967295)
    string = ("0000000000000000000000" + format(value, "b"))[-22:]
    msgs = format(ret, "b") + string
    return str(int(msgs, 2))
    
def decimal_to_base36(number: int) -> str:
    """Convert decimal to base36."""
    if number == 0:
        return "0"
        
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    result = ""
        
    while number:
        number, remainder = divmod(number, 36)
        result = digits[remainder] + result
        
    return result
    
    
    

def parse_json_safe(content: str) -> Dict[str, Any]:
    """Safely parse JSON content."""
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        raise ValidationError(f"Error parsing JSON: {e}", details={'content': content[:200]}) from e
    
    
def prefix_url(url: str, host: str) -> str:
    """Add protocol and host prefix to URL if needed."""
    if url.startswith("/"):
        return f"https://{host}{url}"
    return url
    
    
def mimetype_to_key(mimetype: Optional[str]) -> str:
    """Convert MIME type to Facebook's attachment key format."""
    if not mimetype:
        return "file_id"
    if mimetype == "image/gif":
        return "gif_id"

    parts = mimetype.split("/")
    if parts[0] in ["video", "image", "audio"]:
        return f"{parts[0]}_id"
    return "file_id"
    

def get_jsmods_require(response: Dict[str, Any], index: int) -> Optional[str]:
    """Extract jsmods require data from Facebook response."""
    try:
        return response["jsmods"]["require"][0][index][0]
    except (KeyError, IndexError, TypeError):
        return None

