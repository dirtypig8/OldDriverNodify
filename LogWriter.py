import logging
import logging.handlers
import os


class FormattedLog:
    def __init__(self):
        self.log_format = '%(levelname)-7s - %(asctime)s - %(message)s'
        self.date_format = '%Y/%m/%d %H:%M:%S'


class BasicLoggerConfigurator:
    def __init__(self):
        self.__logger = None

    def config_basic_writer(self, log_path):
        self.__do_basic_config()

        self.__logger = logging.getLogger()

        handler = self.__get_handler(log_path)
        self.__logger.addHandler(handler)

    @staticmethod
    def __do_basic_config():
        logging.basicConfig(level=logging.DEBUG,
                            format=FormattedLog().log_format,
                            datefmt=FormattedLog().date_format)

    @staticmethod
    def __get_handler(log_path):
        log_directory = os.path.dirname(log_path)
        os.makedirs(name=log_directory, exist_ok=True)

        handler = logging.handlers.TimedRotatingFileHandler(filename=log_path, when='midnight')
        handler.setLevel(logging.NOTSET)
        formatter = logging.Formatter(fmt=FormattedLog().log_format, datefmt=FormattedLog().date_format)
        handler.setFormatter(formatter)

        return handler


class LogWriter:
    def __init__(self):
        self.__logger = logging.getLogger()

    def write_log(self, message):
        self.__logger.info(message)

    def write_warning(self, message):
        self.__logger.warning(message)
