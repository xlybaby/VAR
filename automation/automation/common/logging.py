# -*- coding: utf-8 -*-

import threading,logging,re
from logging.handlers import TimedRotatingFileHandler
from logging.handlers import RotatingFileHandler

from automation.common.application import Configure

class Logger(object):
  #_instance_lock = threading.Lock()
  logger=None
  
  def __init__(self):
    self._level = {"INFO":logging.INFO, "WARNING":logging.WARNING, "DEBUG":logging.DEBUG, "ERROR":logging.ERROR}
    logdir = Configure.configure().value(p_key="logger.dir")
    loglevel = Configure.configure().value(p_key="logger.level")
    logunit = Configure.configure().value(p_key="logger.keepUnit")
    loginterval = Configure.configure().value(p_key="logger.keepInterval")
    logcount = Configure.configure().value(p_key="logger.keepCount")
        
    log_fmt = '%(asctime)s\tFile \"%(filename)s\"%(levelname)s: %(message)s'
    formatter = logging.Formatter(log_fmt)
    log_file_handler = TimedRotatingFileHandler(filename=logdir, when=logunit, interval=loginterval, backupCount=logcount)
    log_file_handler.suffix = "%Y-%m-%d"
    #log_file_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")
    log_file_handler.setFormatter(formatter)
    logging.basicConfig(level=self._level[loglevel.upper()])
    Logger.logger = logging.getLogger()
    Logger.logger.addHandler(log_file_handler)
    
    logging.getLogger('apscheduler').setLevel(logging.ERROR)
    
  @staticmethod  
  def getLogger():
    return Logger.logger
 
#   def __new__(cls, *args, **kwargs):
#     if not hasattr(Logger, "_instance"):
#       with Logger._instance_lock:
#         if not hasattr(Logger, "_instance"):
#           Logger._instance = object.__new__(cls)  
#     return Logger._instance