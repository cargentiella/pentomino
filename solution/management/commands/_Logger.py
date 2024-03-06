import logging
import sys


def set_logger(name):
    # set the logging level
    level = logging.INFO
    # specify the layout of log records
    formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    logging.basicConfig(
        level=level,
        format=formatter, 
        stream=sys.stdout,
    )

    logger = logging.getLogger(name)

    return logger
