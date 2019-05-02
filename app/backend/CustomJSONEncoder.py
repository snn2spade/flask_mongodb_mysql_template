import datetime
import json

import numpy as np
from bson import ObjectId

from ConfigLoader import AppConfig


class CustomJSONEncoder(json.JSONEncoder):

    def default(self, o):
        # log.debug("CustomJSONEncoder has been called")
        if isinstance(o, ObjectId):
            return str(o)
        elif isinstance(o, datetime.datetime):
            return o.strftime(AppConfig().config["DATETIME_FORMAT"])
        elif isinstance(o, datetime.date):
            return o.strftime(AppConfig().config["DATE_FORMAT"])
        elif isinstance(o, np.int64):
            return int(o)

        return json.JSONEncoder.default(self, o)
