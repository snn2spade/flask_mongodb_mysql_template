import datetime
import json
import os

from logging.config import dictConfig


class LoggerLoader:
    @classmethod
    def load_config_json(cls, text):
        date_tag = datetime.datetime.now().strftime("%Y-%m-%d")
        config = json.load(text)
        config['handlers']['info_file_handler']['filename'] = "log/%s_%s.log" % (
            config['handlers']['info_file_handler']['filename'], date_tag)
        config['handlers']['error_file_handler']['filename'] = "log/%s_%s.log" % (
            config['handlers']['error_file_handler']['filename'], date_tag)
        dictConfig(config)

    def __init__(self):
        # Create log folder
        if not os.path.exists("log"):
            os.makedirs("log")

        try:
            with open('logging_config.json', 'rt') as f:
                self.load_config_json(f)
        except FileNotFoundError:
            try:
                with open('../logging_config.json', 'rt') as f:
                    self.load_config_json(f)
            except FileNotFoundError:
                print("[WARN]: Not found logging config file, this will disable logging")
