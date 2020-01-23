import json
from datetime import datetime
from unittest.mock import MagicMock

import pytest

from app.backend.util.custom_json_decoder import get_custom_json_decoder


@pytest.fixture
def custom_json_decoder() -> json.JSONDecoder:
    app_config = MagicMock(config={
        "DECODER": {
            "DATE_TIME_FORMAT": [
                "%Y-%m-%dT%H:%M:%SZ",
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%d"
            ]
        }
    })
    return get_custom_json_decoder(app_config)()


def test_generic_type(custom_json_decoder: json.JSONDecoder):
    incoming_json = '{"boolean": true, "int": 1, "float": 2.5,"none": null}'
    assert custom_json_decoder.decode(incoming_json) == {
        "boolean": True,
        "int": 1,
        "float": 2.5,
        "none": None
    }


def test_custom_type(custom_json_decoder: json.JSONDecoder):
    incoming_json = '{"date": "2018-01-01", "datetime": "2019-01-01T16:00:00"}'
    assert custom_json_decoder.decode(incoming_json) == {
        "date": datetime(2018, 1, 1),
        "datetime": datetime(2019, 1, 1, 16, 0, 0)
    }
