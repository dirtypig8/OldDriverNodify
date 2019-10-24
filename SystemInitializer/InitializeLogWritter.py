from CoreConfig.ConfigDictionary import ConfigDictionary
from LogWriter import BasicLoggerConfigurator


class InitializeLogWriter:
    @staticmethod
    def execute():
        BasicLoggerConfigurator().config_basic_writer(log_path=ConfigDictionary().config_dict["log_path"])
