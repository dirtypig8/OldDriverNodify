from CoreConfig.ConfigsFromFile import ConfigsFromFile
from CoreConfig.ConfigDictionary import ConfigDictionary


class InitializeConfigDictionary:
    @staticmethod
    def execute(config_file_path):
        try:
            ConfigsFromFile().read_configs(config_file_path)
            ConfigDictionary().initialize_config_dict()
        except Exception:
            raise


if __name__ == '__main__':
    obj = InitializeConfigDictionary.execute("../config.ini")