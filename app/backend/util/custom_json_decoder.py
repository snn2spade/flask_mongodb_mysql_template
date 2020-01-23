import datetime
import json
from typing import Callable, Any, Type

from app.config_loader import AppConfig


def get_custom_json_decoder(app_config: AppConfig) -> Type[json.JSONDecoder]:
    class CustomJSONDecoder(json.JSONDecoder):
        def __init__(self, *args, **kwargs):
            json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

        @classmethod
        def apply_function(cls, target_obj: dict, func: Callable[[dict], Any]):
            for k, v in target_obj.items():
                if isinstance(v, dict):
                    cls.apply_function(target_obj[k], func)
                else:
                    target_obj[k] = func(v)

        @classmethod
        def apply_function_on_dict(cls, target_obj, func: Callable[[dict], Any]):
            for k, v in target_obj.items():
                if isinstance(v, dict):
                    cls.apply_function_on_dict(target_obj[k], func)
                    target_obj[k] = func(v)

        @classmethod
        def extract_date_timezone(cls, obj: dict):
            if isinstance(obj, dict) and "date" in obj and "timezone" in obj:
                return cls.extract_date_time(obj["date"])
            else:
                return obj

        @classmethod
        def extract_date_time(cls, text: object):
            for date_time_format in app_config.config["DECODER"]["DATE_TIME_FORMAT"]:
                try:
                    return datetime.datetime.strptime(str(text), date_time_format)
                except ValueError:
                    continue
            return text

        def object_hook(self, obj):
            # log.debug("CustomJSONDecoder has been called")
            self.apply_function(obj, self.extract_date_time)
            self.apply_function_on_dict(obj, self.extract_date_timezone)
            return obj

    return CustomJSONDecoder
