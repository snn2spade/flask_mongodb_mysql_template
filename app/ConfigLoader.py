import json
from pathlib import Path


class Singleton(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class AppConfig(metaclass=Singleton):
    config = {}

    def __init__(self):
        try:
            with open('app_config.json', 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            try:
                with open('../app_config.json', 'r') as f:
                    self.config = json.load(f)
            except FileNotFoundError:
                with open(Path(__file__).parent.parent.joinpath('app_config.json'), 'r') as f:
                    self.config = json.load(f)
