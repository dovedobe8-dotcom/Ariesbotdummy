from msgspec import Struct, Raw

class LSResp(Struct, frozen=True, eq=False):
    request_id: int
    """Id of the sent request. Used to keep track of requests"""
    payload: str
    """Kind of like a pointer pointing to raw bytes of the payload in the memory for later decoding"""




