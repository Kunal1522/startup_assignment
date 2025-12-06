import logging
import sys
from datetime import datetime
from enum import Enum
from typing import Optional, Any


class LogLevel(Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class AppLogger:
    _instances = {}
    _initialized = False

    def __new__(cls, name: str = 'app'):
        if name not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[name] = instance
        return cls._instances[name]

    def __init__(self, name: str = 'app'):
        if hasattr(self, '_logger'):
            return
        
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.DEBUG)
        
        if not self._logger.handlers:
            formatter = logging.Formatter(
                '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.DEBUG)
            console_handler.setFormatter(formatter)
            self._logger.addHandler(console_handler)

    def _format_message(self, message: str, context: Optional[dict] = None) -> str:
        if context:
            context_str = ' | '.join(f'{k}={v}' for k, v in context.items())
            return f'{message} | {context_str}'
        return message

    def debug(self, message: str, context: Optional[dict] = None) -> None:
        self._logger.debug(self._format_message(message, context))

    def info(self, message: str, context: Optional[dict] = None) -> None:
        self._logger.info(self._format_message(message, context))

    def warning(self, message: str, context: Optional[dict] = None) -> None:
        self._logger.warning(self._format_message(message, context))

    def error(self, message: str, exception: Optional[Exception] = None, context: Optional[dict] = None) -> None:
        msg = self._format_message(message, context)
        if exception:
            msg = f'{msg} | exception={type(exception).__name__}: {str(exception)}'
        self._logger.error(msg, exc_info=exception is not None)

    def critical(self, message: str, exception: Optional[Exception] = None, context: Optional[dict] = None) -> None:
        msg = self._format_message(message, context)
        if exception:
            msg = f'{msg} | exception={type(exception).__name__}: {str(exception)}'
        self._logger.critical(msg, exc_info=True)
