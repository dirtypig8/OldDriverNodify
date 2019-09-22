import os
import configparser


class ConfigsFromFile:
    __configs = configparser.ConfigParser()

    def __init__(self, file_path):
        if os.path.isfile(file_path):
            self.__configs.read(file_path, encoding='utf-8-sig')
        else:
            raise Exception('Config file is not exist.')

    def get_config_if_exist(self, section, option):
        if self.__configs.has_option(section, option):
            value = self.__configs[section][option]
        else:
            raise Exception('Option is not exist.')
        return value
