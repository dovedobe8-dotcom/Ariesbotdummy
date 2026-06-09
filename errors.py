"""
fbchat_muqit/exceptions/errors.py - Custom Exception Classes
"""

from typing import Optional, Dict, Any
import traceback

class FBChatError(Exception):
    """
    Base exception for all fbchat-muqit errors.
    Clean formatting, supports error chaining, and structured data.
    """
    emoji = "❌"

    def __init__(
        self,
        message: str,
        *,
        error_code: Optional[str | int] = None,
        details: Optional[Dict[str, Any]] = None,
        original_exception: Optional[Exception] = None
    ):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        self.original_exception = original_exception

    def __str__(self) -> str:
        base = f"{self.emoji} {self.__class__.__name__}: {self.message}"
        if self.error_code:
            base += f" (Code: {self.error_code})"
        if self.original_exception:
            base += f"\n↳ Caused by: {type(self.original_exception).__name__}: {self.original_exception}"
        return base

    def pretty_trace(self) -> str:
        """Return a detailed traceback string for debug logging."""
        if self.original_exception:
            return "".join(traceback.format_exception(self.original_exception))
        return ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.__class__.__name__,
            "message": self.message,
            "error_code": self.error_code,
            "details": self.details,
        }


# ─────────── Specific Exceptions ───────────

class AuthenticationError(FBChatError): emoji = "🔐"
class LoginError(AuthenticationError): emoji = "🚪"
class SessionExpiredError(AuthenticationError): emoji = "⏰"
class TwoFactorRequiredError(AuthenticationError): emoji = "📲"

class APIError(FBChatError): emoji = "🌐"
class ResponseError(APIError): emoji = "⚠️"
class RateLimitError(APIError): emoji = "⏳"
class NetworkError(APIError): emoji = "📡"
class FacebookAPIError(APIError): emoji = "📘"

class ParsingError(FBChatError): emoji = "🧩"
class MqttMessageParsingError(ParsingError): emoji = "📡"

class MessageError(FBChatError): emoji = "💬"
class MessageSendError(MessageError): emoji = "📤"
class AttachmentError(MessageError): emoji = "📎"

class ThreadError(FBChatError): emoji = "🧵"
class UserNotFoundError(FBChatError): emoji = "👤"

class ConnectionError(FBChatError): emoji = "🔗"
class RealtimeError(ConnectionError): emoji = "⚡"

class ValidationError(FBChatError): emoji = "🧾"
class ConfigurationError(FBChatError): emoji = "⚙️"


# ─────────── Helper Decorator ───────────

def handle_exceptions(default_exception=FBChatError):
    """Decorator to wrap and cleanly log exceptions."""
    def decorator(func):
        import inspect
        if inspect.iscoroutinefunction(func):
            async def wrapper(*args, **kwargs): #type: ignore
                from ..logging.logger import get_logger
                logger = get_logger()
                try:
                    return await func(*args, **kwargs)
                except FBChatError as e:
                    logger.error(str(e))
                    raise
                except Exception as e:
                    err = default_exception(f"Unexpected error in {func.__name__}: {e}", original_exception=e)
                    logger.error(str(err))
                    raise err from e
        else:
            def wrapper(*args, **kwargs):
                from ..logging.logger import get_logger
                logger = get_logger()
                try:
                    return func(*args, **kwargs)
                except FBChatError as e:
                    logger.error(str(e))
                    raise
                except Exception as e:
                    err = default_exception(f"Unexpected error in {func.__name__}: {e}", original_exception=e)
                    logger.error(str(err))
                    raise err from e
        return wrapper
    return decorator

def patch_logger_class(logger_cls):
    """Add exception-aware methods to the logger class."""

    def exception(self, exc: Exception, context: str = ""):
        emoji = getattr(exc, "emoji", "❌")
        msg = f"{emoji} {exc.__class__.__name__}: {exc}"
        context_str = f" ({context})" if context else ""
        self.logger.error(
            f"{msg}{context_str}",
            exc_info=isinstance(exc, Exception),
            extra={'extra_data': {'context': context}},
            )

    logger_cls.exception = exception
    return logger_cls
