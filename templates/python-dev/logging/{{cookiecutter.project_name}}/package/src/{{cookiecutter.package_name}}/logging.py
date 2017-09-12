""" 
Logging helper module based on a subset of the code on the 
python-boilerplate web app https://www.python-boilerplate.com/py3+logging

This helper provides a versatile yet easy to use logging setup. 
You can use it to log to the console and optionally to a logfile.

The call `logger.info("hello")` prints log messages in this format:

    [I 170213 15:02:00 test:203] hello

Usage:

    from logger import setup_logger

    logger = setup_logger()
    logger.info("message")

In order to also log to a file, just add a `logfile` parameter:

    logger = setup_logger(logfile="/tmp/test.log")

The default loglevel is `logging.DEBUG`. You can set it with the
parameter `level`.
"""
import logging


def setup_logger(name=__name__, logfile=None, level=logging.DEBUG):
    """
    A utility function that you can call to easily set up logging to the
    console and optionally to a file. No hassles.
    """
    logger = logging.getLogger(name)
    logger.propagate = False
    logger.setLevel(level)

    # Remove old handlers to allow updating settings
    for handler in list(logger.handlers):
        logger.removeHandler(handler)

    # create console handler
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)  # propagate all messages

    # add the formatter to the handler
    formatter = logging.Formatter('%(name)s - %(asctime)-15s - %(levelname)s: %(message)s')
    stream_handler.setFormatter(formatter)

    # setup logger and add the handlers
    logger.addHandler(stream_handler)

    if logfile:
        filehandler = logging.FileHandler(logfile)
        filehandler.setLevel(logging.NOTSET)
        filehandler.setFormatter(formatter)
        logger.addHandler(filehandler)

    logger.debug("logger set up. level=%d", level)
    return logger
