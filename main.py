"""
main.py — Entry point for the fbchat-muqit Messenger bot.

Authentication:
  Set the FACEBOOK_COOKIES_JSON environment variable to the raw JSON string
  of your Facebook cookies, or place a cookies.json file in the working
  directory.  The environment variable takes precedence.
"""

import json
import logging
import os
import sys
import tempfile

from fbchat_muqit import Client, Message

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Resolve cookie source
# ---------------------------------------------------------------------------

COOKIES_ENV_VAR = "FACEBOOK_COOKIES_JSON"
COOKIES_FILE_DEFAULT = "cookies.json"

_tmp_cookies_file: str | None = None


def _resolve_cookies_path() -> str:
    """Return a path to a cookies JSON file.

    Preference order:
    1. FACEBOOK_COOKIES_JSON env var (raw JSON string) → written to a temp file
    2. cookies.json in the current working directory
    """
    raw_json = os.environ.get(COOKIES_ENV_VAR)
    if raw_json:
        logger.info("Loading Facebook cookies from %s environment variable.", COOKIES_ENV_VAR)
        try:
            # Validate that the value is parseable JSON before writing it out.
            json.loads(raw_json)
        except json.JSONDecodeError as exc:
            logger.error(
                "The value of %s is not valid JSON: %s", COOKIES_ENV_VAR, exc
            )
            sys.exit(1)

        # Write to a temporary file so the library can read it normally.
        global _tmp_cookies_file
        tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, prefix="fb_cookies_"
        )
        tmp.write(raw_json)
        tmp.close()
        _tmp_cookies_file = tmp.name
        return tmp.name

    if os.path.isfile(COOKIES_FILE_DEFAULT):
        logger.info("Loading Facebook cookies from %s.", COOKIES_FILE_DEFAULT)
        return COOKIES_FILE_DEFAULT

    logger.error(
        "No Facebook cookies found. "
        "Set the %s environment variable or place a cookies.json file in the "
        "working directory.",
        COOKIES_ENV_VAR,
    )
    sys.exit(1)


# ---------------------------------------------------------------------------
# Bot setup
# ---------------------------------------------------------------------------

cookies_path = _resolve_cookies_path()
client = Client(cookies_path)


@client.event
async def on_listening() -> None:
    """Fired once the MQTT connection is established and the bot is online."""
    logger.info("Bot is online. Account: %s (uid: %s)", client.name, client.uid)


@client.event
async def on_message(message: Message) -> None:
    """Echo every incoming message back to the same thread."""
    # Ignore messages sent by the bot itself to prevent infinite loops.
    if message.sender_id == client.uid:
        return

    if not message.text:
        return

    logger.info(
        "Message from %s in thread %s: %s",
        message.sender_id,
        message.thread_id,
        message.text,
    )

    try:
        await client.send_message(message.text, message.thread_id)
    except Exception as exc:  # noqa: BLE001
        logger.error(
            "Failed to send echo to thread %s: %s", message.thread_id, exc
        )


@client.event
async def on_error(error: Exception) -> None:
    """Log any errors emitted by the client."""
    logger.error("Client error: %s", error, exc_info=error)


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    logger.info("Starting Messenger bot…")
    try:
        client.run()
    finally:
        # Clean up the temporary cookies file if one was created.
        if _tmp_cookies_file and os.path.exists(_tmp_cookies_file):
            os.unlink(_tmp_cookies_file)
            logger.debug("Removed temporary cookies file %s.", _tmp_cookies_file)
