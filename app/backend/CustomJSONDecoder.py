import datetime
import json

from ConfigLoader import AppConfig


class CustomJSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    @classmethod
    def apply_function(cls, target_obj, func):
        for k, v in target_obj.items():
            if isinstance(v, dict):
                cls.apply_function(target_obj[k], func)
            else:
                target_obj[k] = func(v)

    @classmethod
    def apply_function_on_dict(cls, target_obj, func):
        for k, v in target_obj.items():
            if isinstance(v, dict):
                cls.apply_function_on_dict(target_obj[k], func)
                target_obj[k] = func(v)

    @classmethod
    def extract_date_timezone(cls, obj):
        if isinstance(obj, dict) and "date" in obj and "timezone" in obj:
            return cls.extract_date(obj["date"])
        else:
            return obj

    @classmethod
    def extract_date(cls, text):
        try:
            return datetime.datetime.strptime(str(text), AppConfig().config["DATETIME_FORMAT"])
        except ValueError:
            try:
                return datetime.datetime.strptime(str(text), AppConfig().config["UTC_DATETIME_FORMAT"])
            except ValueError:
                try:
                    return datetime.datetime.strptime(str(text), AppConfig().config["DATE_FORMAT"])
                except ValueError:
                    return text

    def object_hook(self, obj):
        # log.debug("CustomJSONDecoder has been called")
        self.apply_function(obj, self.extract_date)
        self.apply_function_on_dict(obj, self.extract_date_timezone)
        return obj
