import logging
from logging.handlers import RotatingFileHandler

import os
import psutil


class Log:

    SEPARATOR = '|'

    logger = None
    exhibit_name = ''

    @staticmethod
    def init(log_file_path, exhibit_name):
        Log.exhibit_name = exhibit_name

        logging.basicConfig(filename=log_file_path, filemode='a', level=logging.INFO)

        handler = RotatingFileHandler(log_file_path, maxBytes=37500, backupCount=100)
        Log.logger = logging.getLogger(Log.exhibit_name)
        formatter = logging.Formatter('%(asctime)s.%(msecs)03d|%(levelname)s|%(message)s', '%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)
        Log.logger.propagate = False
        Log.logger.addHandler(handler)

    @staticmethod
    def get_logger():
        return Log.logger

    @staticmethod
    def prepare_log_message(message, parts):
        process = psutil.Process(os.getpid())
        memory_usage = int(process.memory_info().rss / float(2 ** 20))
        full_message = Log.exhibit_name + Log.SEPARATOR + str(memory_usage) + 'MB' + Log.SEPARATOR + message
        if len(parts) > 0:
            full_message += (Log.SEPARATOR + Log.SEPARATOR.join(parts))

        return full_message

    @staticmethod
    def info(message, *parts):
        Log.logger.info(Log.prepare_log_message(message, list(parts)))

    @staticmethod
    def error(message, *parts):
        Log.logger.error(Log.prepare_log_message(message, list(parts)))
