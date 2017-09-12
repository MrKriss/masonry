from .logging import setup_logger

logger = setup_logger(logfile=None)

# To get a reference to this logger from other modules:
# logger = logging.getLogger(__name__)
