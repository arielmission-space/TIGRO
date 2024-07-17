import importlib.metadata as metadata
from datetime import date

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
import logging
from paos.log import setLogLevel

logger = logging.getLogger("paos")
setLogLevel(logging.DEBUG)

logger.name = __pkg_name__
logger.info(f"code version {__version__}")
