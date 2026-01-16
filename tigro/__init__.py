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

import matplotlib.pyplot as plt
from loguru import logger

# logger.level("Announce", no=100, color="<magenta>")

# initialise plotter
plt.rcParams["figure.facecolor"] = "white"
plt.rc("lines", linewidth=1.5)
plt.rc(
    "axes",
    axisbelow=True,
    titleweight="bold",
    labelcolor="dimgray",
    labelweight="bold",
)
plt.rc("font", size=12)

import shutil

has_latex = shutil.which("latex") is not None
has_renderer = shutil.which("dvipng") is not None or shutil.which("dvisvgm") is not None

plt.rc("text", usetex=(has_latex and has_renderer))
