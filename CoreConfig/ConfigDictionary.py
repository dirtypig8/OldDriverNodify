from CoreConfig.ConfigsFromFile import *


class ConfigDictionary:
    config_dict = dict()

    @staticmethod
    def initialize_config_dict():
        try:
            ConfigDictionary.config_dict = {
                "line_access_token": ConfigsFromFile().get_value_with_existence_checking(
                    "line", "access_token"
                ),
                "send_random_avid_to_line_sleep": int(
                    ConfigsFromFile().get_value_with_existence_checking("system", "send_random_avid_to_line_sleep")
                ),
                "sync_javbus_sleep": int(
                    ConfigsFromFile().get_value_with_existence_checking("system", "sync_javbus_sleep")
                ),
                "send_new_avid_to_line_sleep": int(
                    ConfigsFromFile().get_value_with_existence_checking("system", "send_new_avid_to_line_sleep")
                ),
                "send_system_info_to_line_sleep": int(
                    ConfigsFromFile().get_value_with_existence_checking("system", "send_system_info_to_line_sleep")
                ),
                "bitly_user": ConfigsFromFile().get_value_with_existence_checking(
                    "bitly", "user"
                ),
                "bitly_key": ConfigsFromFile().get_value_with_existence_checking(
                    "bitly", "key"
                ),
            }

        except Exception:
            print('ConfigDictionary error')