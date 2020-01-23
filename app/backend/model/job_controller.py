from typing import List

from pymongo.results import InsertOneResult

from app.backend.service.mongo_db_connector_service import MongoDBConnectorService
from app.backend.model.job import Job


class JobController:
    def __init__(self, mongo_db_connector_service: MongoDBConnectorService, collection_name='job'):
        self._mongo_db_connector_service = mongo_db_connector_service
        self._collection_name = collection_name

    def insert_one(self, job: Job) -> InsertOneResult:
        db = self._mongo_db_connector_service.get_db()
        return db[self._collection_name].insert_one(job.to_dict())

    def find_all(self) -> List[Job]:
        db = self._mongo_db_connector_service.get_db()
        job_list = db[self._collection_name].find()
        if job_list is None:
            return []
        else:
            return list(map(Job.from_dict, job_list))
