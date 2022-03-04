"""
Swanky logger for all python support scripts
Usage:
          logger = ACQLogger().get_logger()
          logger.critical('Critical message')
          logger.error('Error message')
          logger.warning('Warning message')
          logger.info('Info message')
          logger.debug('Debug message')
"""

import atexit
import logging.config
import os
import time


def mysingleton(cls):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance


@mysingleton
class ACQLogger:

    def __init__(self):
        logrootdir = os.environ['LOGROOTDIR'] if 'LOGROOTDIR' in os.environ else os.environ['HOME'] + '/logs/'

        os.makedirs(logrootdir, exist_ok=True)

        start_time = time.localtime()
        y, m, d = time.strftime('%y', start_time), time.strftime('%m', start_time), time.strftime('%d', start_time)

        log_file_path = logrootdir + y + '/' + m + '/' + d + '/'

        os.makedirs(log_file_path, exist_ok=True)

        self.log_file_name = log_file_path + 'suplog_' + time.strftime('%y%m%d_%H%M%S', start_time) + '.log'

        d = {
            'version': 1,
            'formatters': {
                'detailed': {
                    'class': 'logging.Formatter',
                    'format': '%(asctime)s %(levelname)-8s [%(filename)-30s:%(lineno)-4d] %(message)s'
                }
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'level': 'INFO',
                    'formatter': 'detailed',
                    'stream': 'ext://sys.stdout',
                },
                'file': {
                    'class': 'logging.FileHandler',
                    'level': 'DEBUG',
                    'formatter': 'detailed',
                    'filename': self.log_file_name,
                    'mode': 'a',
                },
            },
            'root': {
                'level': 'DEBUG',
                'handlers': ['console', 'file']
            },
        }

        logging.config.dictConfig(d)
        self.logger = logging.getLogger(__name__)

        self.print_log_name()

        atexit.register(self.print_log_name)

    def print_log_name(self):
        self.logger.info(self.log_file_name)

    def get_logger(self):
        return self.logger

    def get_log_file_name(self):
        return self.log_file_name
