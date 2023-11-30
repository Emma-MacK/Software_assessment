# importing module
import logging
import logging.handlers as handlers
import os #this is just imported as a place holder for when we want to specify the exact storage location of the runlog
import time

# setting the logging.Formatter to use GMT time as default. This will guarantee that the log file reflects UK local time even when staff are abroad
logging.Formatter.converter = time.gmtime

# create logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# creating formatter
formatter = logging.Formatter("%(asctime)s, %(levelname)s, %(message)s",
                              datefmt="%Y-%m-%d %H:%M:%S %Z")

# creating rotating file handler and set level to debug
file_handler = handlers.RotatingFileHandler('runlog.log', maxBytes=500000, backupCount=5)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# creating stream handler and set level to Error
console_log = logging.StreamHandler()
console_log.setLevel(logging.ERROR)
console_log.setFormatter(formatter)

# Adding handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_log)

#testing logger
logger.debug("Is it working?")
logger.info("The logger is running")
logger.warning("This will not print to console")
logger.error("This will print to console")
logger.critical("This will result in the programm not continuing")

# # example of logging.info to be added to our files.
# logging.info("Argument %s: %r", arg, value)


# ## OLD
# # create and configure logger
# logging.basicConfig(filename="logging.log",
#                     format="%(asctime)s, %(levelname)s, %(message)s",
#                     datefmt="%Y-%m-%d %H:%M:%S",
#                     level=logging.DEBUG)
# # logging.Formatter.formatTime = time.gmtime
# logger = logging.getLogger()

# # testing logger
# logger.info("Is it working?")

# # # logging drafts
# # for arg, value in sorted(vars(args).items()):
# #     logging.info("Argument %s: %r", arg, value)