"""
fbchat_muqit/logging/logger.py - Enhanced Logging System
"""

import json
import logging
import sys
from datetime import datetime
from enum import Enum
from typing import Any, Optional, Union


class LogLevel(Enum):
    TRACE = 5
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50
    API_REQUEST = 15
    API_RESPONSE = 16
    MESSAGE = 25
    CONNECTION = 35


class ColoredFormatter(logging.Formatter):
    FRAG = {
        "RESET": "\033[0m",
        "TS": "\033[90m",  # timestamp -> grey
        "SEPARATOR": "\033[90m",
        "LOGGER": "\033[38;5;214m",  # orange-ish
    }

    LEVEL_COLORS = {
        "TRACE": "\033[90m",
        "DEBUG": "\033[94m",
        "API_REQUEST": "\033[96m",
        "API_RESPONSE": "\033[36m",
        "INFO": "\033[92m",
        "MESSAGE": "\033[93m",
        "WARNING": "\033[93m",
        "CONNECTION": "\033[95m",
        "ERROR": "\033[91m",
        "CRITICAL": "\033[91m\033[1m",
    }

    # Message text colors (NEW)
    MESSAGE_COLORS = {
        "TRACE": "\033[90m",
        "DEBUG": "\033[37m",
        "API_REQUEST": "\033[96m",
        "API_RESPONSE": "\033[36m",
        "INFO": "\033[92m",
        "MESSAGE": "\033[93m",
        "WARNING": "\033[93m",
        "CONNECTION": "\033[95m",
        "ERROR": "\033[91m",
        "CRITICAL": "\033[91m\033[1m",
    }

    EMOJIS = {
        "TRACE": "🔍",
        "DEBUG": "🐛",
        "API_REQUEST": "📤",
        "API_RESPONSE": "📥",
        "INFO": "📜",
        "MESSAGE": "💬",
        "WARNING": "⚠️",
        "CONNECTION": "🔗",
        "ERROR": "❌",
        "CRITICAL": "💥",
    }

    def format(self, record):
        ts = datetime.fromtimestamp(record.created).strftime("%H:%M:%S.%f")[:-3]
        level = record.levelname

        emoji = self.EMOJIS.get(level, "📝")
        reset = self.FRAG["RESET"]

        ts_color = f"{self.FRAG['TS']}{ts}{reset}"
        sep = self.FRAG["SEPARATOR"]

        level_color = f"{self.LEVEL_COLORS.get(level, '')}{level}{reset}"

        logger_color = f"{self.FRAG['LOGGER']}{record.name}{reset}"

        # NEW: colorize message using MESSAGE_COLORS
        msg_raw = super().format(record)
        msg_color = f"{self.MESSAGE_COLORS.get(level, '')}{msg_raw}{reset}"

        caller = (
            f" [{record.filename}:{record.lineno}]"
            if record.levelno <= logging.DEBUG
            else ""
        )

        return (
            f"{emoji} "
            f"{ts_color} {sep}|{reset} "
            f"{level_color} {sep}|{reset} "
            f"{logger_color}{caller} {sep}|{reset} "
            f"{msg_color}"
        )


class JSONFormatter(logging.Formatter):
    def format(self, record):
        entry = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }
        if record.exc_info:
            entry['exception'] = self.formatException(record.exc_info)
        if hasattr(record, 'extra_data'):
            entry['extra'] = record.extra_data #type: ignore
        return json.dumps(entry, ensure_ascii=False)


class FBChatLogger:
    def __init__(
        self,
        name: str = "fbchat-muqit",
        level: Union[int, str, LogLevel] = LogLevel.INFO,
        console_output: bool = True,
        enable_colors: bool = True,
        log_api_requests: bool = True,
        log_api_responses: bool = False,
        sensitive_fields: Optional[list] = None
    ):
        self.name = name
        self.sensitive_fields = sensitive_fields or ['password', 'token', 'access_token', 'session', "email", "fb_dtsg", "lsd"]
        self.log_api_requests = log_api_requests
        self.log_api_responses = log_api_responses

        self.logger = logging.getLogger(name)
        self.logger.setLevel(self._convert_level(level))
        self._add_custom_levels()
        self.logger.handlers.clear()

        if console_output:
            self._setup_console_handler(enable_colors)

    def _convert_level(self, level):
        if isinstance(level, LogLevel):
            return level.value
        if isinstance(level, str):
            return getattr(logging, level.upper(), logging.INFO)
        return level

    def _add_custom_levels(self):
        for lvl in LogLevel:
            logging.addLevelName(lvl.value, lvl.name)
            method = lvl.name.lower()
            if not hasattr(self.logger, method):
                setattr(self.logger, method, lambda msg, *a, lvl=lvl.value, **kw: self.logger.log(lvl, msg, *a, **kw))

    def _setup_console_handler(self, enable_colors: bool):
        handler = logging.StreamHandler(sys.stdout)
        formatter = ColoredFormatter() if enable_colors and sys.stdout.isatty() else logging.Formatter('%(asctime)s | %(levelname)-12s | %(name)s | %(message)s', '%H:%M:%S')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def _sanitize_data(self, data: Any) -> Any:
        if isinstance(data, dict):
            return {k: ("***REDACTED***" if any(s in k.lower() for s in self.sensitive_fields) else self._sanitize_data(v)) for k, v in data.items()}
        if isinstance(data, (list, tuple)):
            return [self._sanitize_data(i) for i in data]
        return data

    # ─────────── Logging Methods ───────────

    def debug(self, msg: str, *a, **kw): self.logger.debug(msg, stacklevel=2, *a, **kw)
    def info(self, msg: str, *a, **kw): self.logger.info(msg, stacklevel=2, *a, **kw)
    def warning(self, msg: str, *a, **kw): self.logger.warning(msg, stacklevel=2, *a, **kw)
    def trace(self, msg: str, *a, **kw): self.logger.log(LogLevel.TRACE.value, msg, stacklevel=2, *a, **kw)

    def error(self, msg: str, *a, exc_info=None, **kw):
        prefix = "❌ " if not msg.startswith(("❌", "⚠️", "💥")) else ""
        self.logger.error(prefix + msg, *a, exc_info=exc_info, stacklevel=2, **kw)

    def critical(self, msg: str, *a, **kw): self.logger.critical("💥 " + msg, *a, **kw)

    def exception(self, exc: Exception, context: str = ""):
        emoji = getattr(exc, "emoji", "❌")
        msg = f"{emoji} {exc.__class__.__name__}: {exc}"
        ctx = f" ({context})" if context else ""
        self.logger.error(f"{msg}{ctx}", exc_info=True, extra={'extra_data': {'context': context}})

    # ─────────── Specialized Logging ───────────

    def log_api_request(self, method: str, url: str, data: Any = None, headers: Any = None):
        if not self.log_api_requests: return
        sanitized = self._sanitize_data(data) if data else None
        self.logger.log(LogLevel.API_REQUEST.value, f"📤 API Request: {method} {url}", extra={'extra_data': {'data': sanitized}})

    def log_api_response(self, status: int, url: str, resp: Any = None, duration: float | None = None):
        if not self.log_api_responses: return
        sanitized = self._sanitize_data(resp) if resp else None
        dur = f" ({duration:.3f}s)" if duration else ""
        self.logger.log(LogLevel.API_RESPONSE.value, f"📥 API Response: {status} {url}{dur}", extra={'extra_data': {'response': sanitized, 'duration': duration}})

    def log_connection_event(self, event: str, details: Any = None):
        self.logger.log(LogLevel.CONNECTION.value, f"🔗 Connection: {event}", extra={'extra_data': {'details': details}})

    def log_message_event(self, event_type: str, data: Any = None):
        sanitized = self._sanitize_data(data) if data else None
        self.logger.log(LogLevel.MESSAGE.value, f"💬 Message Event: {event_type}", extra={'extra_data': {'data': sanitized}})


# ─────────── Global Utilities ───────────

global_logger: Optional[FBChatLogger] = None

def get_logger() -> FBChatLogger:
    global global_logger
    if global_logger is None:
        global_logger = FBChatLogger()
    return global_logger

def setup_logger(level: Union[int, str, LogLevel] = LogLevel.INFO, console_output: bool = True, enable_colors: bool = True, **kw) -> FBChatLogger:
    global global_logger
    global_logger = FBChatLogger(level=level, console_output=console_output, enable_colors=enable_colors, **kw)
    return global_logger

def set_log_level(level: Union[int, str, LogLevel]):
    log = get_logger()
    val = level.value if isinstance(level, LogLevel) else getattr(logging, str(level).upper(), logging.INFO)
    log.logger.setLevel(val)

def enable_debug(): set_log_level(LogLevel.DEBUG)
def enable_trace(): set_log_level(LogLevel.TRACE)
def disable_logging(): set_log_level(logging.CRITICAL + 10)

def get_current_log_level() -> str:
    lvl = get_logger().logger.getEffectiveLevel()
    for l in LogLevel:
        if l.value == lvl:
            return l.name
    return logging.getLevelName(lvl)
