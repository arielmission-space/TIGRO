import sys
from loguru import logger

logger.remove()
logger.add(sys.stdout, format="{time:YYYYMMDD HH:mm:ss} | {message}")

__all__ = ["logger"]
