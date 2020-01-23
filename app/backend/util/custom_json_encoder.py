import datetime
import json
from typing import Type

import numpy as np
from bson import ObjectId

from app.config_loader import AppConfig


def get_custom_json_encoder(app_config: AppConfig) -> Type[json.JSONEncoder]:
    class CustomJSONEncoder(json.JSONEncoder):

        def default(self, o: object):
            # log.debug("CustomJSONEncoder has been called")
            if isinstance(o, ObjectId):
                return str(o)
            elif isinstance(o, datetime.datetime):
                return o.strftime(app_config.config["ENCODER"]["DATE_TIME_FORMAT"])
            elif isinstance(o, datetime.date):
                return o.strftime(app_config.config["ENCODER"]["DATE_FORMAT"])
            elif isinstance(o, np.int64):
                return int(o)

            return json.JSONEncoder.default(self, o)

    return CustomJSONEncoder
