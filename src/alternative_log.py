import logging
import logging.config
import logging.handlers as handlers
import time

# setting the logging.Formatter to use GMT time as default. This will guarantee that the log file reflects UK local time even when staff are abroad
logging.Formatter.converter = time.gmtime

# loading logging configuration from the file
logging.config.fileConfig('logging.conf')

# create or get logger
logger = logging.getLogger()

#testing logger
logger.debug("Is it working?")
logger.info("The logger is running")
logger.warning("This will not print to console")
logger.error("This will print to console")
logger.critical("This will result in the programm not continuing")