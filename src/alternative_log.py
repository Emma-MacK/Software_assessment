import logging
import logging.config
import logging.handlers as handlers
import time

# setting the logging.Formatter to use GMT time as default.
# Guarantees that the log file always reflects UK local time
logging.Formatter.converter = time.gmtime

# loading logging configuration from the file
logging.config.fileConfig('Draft_scripts/logging.conf') # TODO this file path will need to be updated once the file directory has been finalised

# create or get logger
logger = logging.getLogger()

#testing logger
logger.debug("Is it working?")
logger.info("The logger is running")
logger.warning("This will not print to console")
logger.error("This will print to console")
logger.critical("This will result in the program not continuing")
