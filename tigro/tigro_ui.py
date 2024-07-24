import os

from shiny import run_app

from tigro import __pkg_name__
from tigro import __version__
from tigro import logger


def main():
    app = os.path.join(os.path.realpath(os.path.dirname(__file__)), "ui", "app.py")
    logger.info(f"Running app: {__pkg_name__} v{__version__}")
    run_app(app, reload=True, launch_browser=False)


if __name__ == "__main__":
    main()
