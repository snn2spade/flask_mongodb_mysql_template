from typing import List

from pymongo.results import InsertOneResult

from app.backend.service.mongo_db_connector_service import MongoDBConnectorService
from app.backend.model.todo import Todo


class TodoController:
    def __init__(self, mongo_db_connector_service: MongoDBConnectorService, collection_name='todo'):
        self._mongo_db_connector_service = mongo_db_connector_service
        self._collection_name = collection_name

    def insert_one(self, todo: Todo) -> InsertOneResult:
        db = self._mongo_db_connector_service.get_db()
        return db[self._collection_name].insert_one(todo.to_dict())

    def find_all(self) -> List[Todo]:
        db = self._mongo_db_connector_service.get_db()
        todo_list = db[self._collection_name].find()
        if todo_list is None:
            return []
        else:
            return list(map(Todo.from_dict, todo_list))
