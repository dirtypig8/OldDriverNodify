import os
import sys
from abc import ABCMeta, abstractmethod


class DefaultValueGetterInterface(metaclass=ABCMeta):
    @abstractmethod
    def execute(self):
        pass


class ApplicationPathGetter(DefaultValueGetterInterface):
    def execute(self):
        if getattr(sys, 'frozen', False):
            application_path = sys.executable

        elif hasattr(sys.modules['__main__'], "__file__"):
            application_path = os.path.abspath(sys.modules['__main__'].__file__)

        else:
            application_path = sys.executable

        return os.path.dirname(application_path)


class DefaultDBPathGetter(DefaultValueGetterInterface):
    def execute(self):
        application_path = ApplicationPathGetter().execute()

        directory_name = "AccessData.sqlite"
        directory_path = os.path.join(application_path, directory_name)

        return directory_path


class DefaultPictureDirectoryPathGetter(DefaultValueGetterInterface):
    def execute(self):
        application_path = ApplicationPathGetter().execute()

        directory_name = "Pictures"
        directory_path = os.path.join(application_path, directory_name)

        return directory_path


class DefaultConfigPathGetter(DefaultValueGetterInterface):
    def execute(self):
        application_path = ApplicationPathGetter().execute()

        config_file_name = "config.ini"
        config_file_path = os.path.join(application_path, config_file_name)

        return config_file_path


class DefaultLogPathGetter(DefaultValueGetterInterface):
    def execute(self):
        application_path = ApplicationPathGetter().execute()

        log_file_name = "OldDriverNodify"
        directory_of_log_file = "Logs"

        log_file_path = os.path.join(application_path, directory_of_log_file)
        log_file_path = os.path.join(log_file_path, log_file_name)

        return log_file_path
