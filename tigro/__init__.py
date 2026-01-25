import importlib.metadata as metadata
from datetime import date
import sys

from .__version__ import __version__

# load package info
__pkg_name__ = metadata.metadata("tigro")["Name"]
__url__ = metadata.metadata("tigro")["Home-page"]
__author__ = metadata.metadata("tigro")["Author"]
__email__ = metadata.metadata("tigro")["Author_email"]
__license__ = metadata.metadata("tigro")["license"]
__copyright__ = "2024-{:d}, {}".format(date.today().year, __author__)
__summary__ = metadata.metadata("tigro")["Summary"]

# initialise logger
# from loguru import logger
# logger.remove()
# logger.add(sys.stdout, format="{time:YYYYMMDD HH:mm:ss} | {message}")


from .logging import logger
from . import io
from . import utils
from . import core


__all__ = ["io", "utils", "logger", "core"]
