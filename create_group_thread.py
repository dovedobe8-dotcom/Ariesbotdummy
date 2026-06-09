import re

def extract_thread_id_raw(data: str) -> str | None:
    """Extract (temp_id, real_id) from LSResp payload using regex without decoding JSON."""
    # Regex to match:
    # "replaceOptimisticThread",[19,"<temp_id>"],[19,"<real_id>"]
    match = re.search(
        r'"replaceOptimisticThread"\s*,\s*\[19,"(\d+)"\]\s*,\s*\[19,"(\d+)"\]',
        data
    )
    if match:
        temp_id, real_id = match.groups()
        return real_id
    return None
