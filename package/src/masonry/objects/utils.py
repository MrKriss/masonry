
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

    logger.debug("logger set up. level=%s", level)
    return logger
