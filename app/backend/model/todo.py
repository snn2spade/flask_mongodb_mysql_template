import copy
from datetime import datetime
from typing import Optional

from bson import ObjectId


class Todo:
    def __init__(self,
                 title: str = None,
                 todo_dict: dict = None):
        if todo_dict is not None:
            self._dict = todo_dict
        else:
            self._dict = {
                "title": title,
                "created_date": datetime.now(),
            }

    def get_id(self) -> Optional[ObjectId]:
        return self._dict.get("_id")

    def get_title(self) -> str:
        return self._dict.get("title")

    def get_created_date(self) -> Optional[datetime]:
        return self._dict.get("created_date")

    @staticmethod
    def from_dict(todo_dict: dict):
        return Todo(todo_dict=todo_dict)

    def to_dict(self):
        return copy.deepcopy(self._dict)
