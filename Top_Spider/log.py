
# -*- encoding= utf-8 -*-
import logging
import logging.handlers
import os
import sys

LOG_LEVELS = {
    
    'NOTSET': logging.NOTSET,
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}


def config_logging( file_name,log_level,logs_dir ):
    '''
    @summary: config logging to write logs to local file
    @param file_name: name of log file
    @param log_level: log level
    '''

    if not logs_dir:
        logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    if os.path.exists(logs_dir) and os.path.isdir(logs_dir):
        pass
    else:
        os.makedirs(logs_dir)

    file_name = os.path.join(logs_dir, file_name)

    #set a logfile rotating function
    rotatingFileHandler = logging.FileHandler( filename =file_name)
    formatter = logging.Formatter("%(asctime)s %(name)-12s %(lineno)3d %(levelname)-8s %(message)s")
    rotatingFileHandler.setFormatter(formatter)
    logging.getLogger().addHandler(rotatingFileHandler)

    console = logging.StreamHandler()  #控制台输出
    formatter = logging.Formatter("%(name)-12s: %(lineno)d %(levelname)-8s %(message)s") 
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)

    logger = logging.getLogger("")
    level = LOG_LEVELS [ log_level.upper() ]
    logger.setLevel(level)


