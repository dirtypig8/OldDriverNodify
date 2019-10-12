import argparse
from CoreConfig.DefaultValues import DefaultConfigPathGetter


class ArgParser:
    def __init__(self):
        self.__parser = argparse.ArgumentParser()

        self.__parser.add_argument('--config-path',
                                   help='path of config file',
                                   dest='config_path',
                                   default=DefaultConfigPathGetter().execute())

        self.__args = self.__parser.parse_args()

    def get_args(self):
        return self.__args
