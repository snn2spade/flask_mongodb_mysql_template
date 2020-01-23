import json
from datetime import datetime, date
from unittest.mock import MagicMock

import pytest

from app.backend.util.custom_json_encoder import get_custom_json_encoder


@pytest.fixture
def custom_json_encoder() -> json.JSONEncoder:
    app_config = MagicMock(config={
        "ENCODER": {
            "DATE_TIME_FORMAT": "%Y-%m-%dT%H:%M:%SZ",
            "DATE_FORMAT": "%Y-%m-%d"
        }
    })
    return get_custom_json_encoder(app_config)()


def test_generic_type(custom_json_encoder: json.JSONEncoder):
    outgoing_dict: dict = {"boolean": True, "int": 1, "float": 2.5, "none": None}
    assert custom_json_encoder.encode(outgoing_dict) == '{"boolean": true, "int": 1, "float": 2.5, "none": null}'


def test_custom_type(custom_json_encoder: json.JSONEncoder):
    outgoing_dict: dict = {
        "date": date(2018, 1, 1),
        "datetime": datetime(2019, 1, 1, 16, 0, 0)
    }
    assert custom_json_encoder.encode(
        outgoing_dict) == '{"date": "2018-01-01", "datetime": "2019-01-01T16:00:00Z"}'
