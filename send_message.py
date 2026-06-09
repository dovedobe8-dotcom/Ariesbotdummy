def extract_message_id_raw(payload: str) -> str | None:
    marker = "replaceOptimsiticMessage"
    idx = payload.find(marker)
    if idx == -1:
        return None
    # Find next "mid." after the marker
    mid_start = payload.find("mid.", idx)
    if mid_start == -1:
        return None
    mid_end = payload.find('"', mid_start)
    return payload[mid_start:mid_end] if mid_end != -1 else None

