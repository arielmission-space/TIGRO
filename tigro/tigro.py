import shutil

from tigro import __pkg_name__
from tigro import __version__
from tigro import logger
from tigro.core.run import run


def main():
    import argparse
    from pathlib import Path
    from time import time as timer

    start = timer()
    logger.info(f"Starting {__pkg_name__} v{__version__}")

    parser = argparse.ArgumentParser(description="Run TIGRO on a configuration file")

    parser.add_argument(
        "-c",
        "--config",
        dest="config",
        type=str,
        required=True,
        default=None,
        help="Path to the configuration file",
    )

    parser.add_argument(
        "-o",
        "--outpath",
        dest="outpath",
        type=str,
        required=True,
        help="Path to the output directory",
    )

    parser.add_argument(
        "-d",
        "--debug",
        dest="debug",
        required=False,
        action="store_true",
        help="Enable debug mode",
    )

    parser.add_argument(
        "-l",
        "--log",
        dest="log",
        default=False,
        required=False,
        action="store_true",
        help="Enable logging to file",
    )

    args = parser.parse_args()

    logger.info(f"Configuration file: {args.config}")

    Path(args.outpath).mkdir(parents=True, exist_ok=True)
    logger.info(f"Output directory: {args.outpath}")

    shutil.copy(args.config, args.outpath)
    logger.info(f"Configuration file copied to {args.outpath}")

    if args.debug:
        logger.setLevel("DEBUG")
        logger.info("Debug mode enabled")

    if args.log:
        logfile = Path(args.outpath) / f"{__pkg_name__}.log"
        from paos.log import addLogFile

        addLogFile(fname=logfile, reset=True, level=logger.level)
        logger.info("Logging to file enabled")

    run(args.config, args.outpath)

    end = timer()
    logger.info(f"Finished in {end - start:.2f} seconds")


if __name__ == "__main__":
    main()
