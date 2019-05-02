import datetime
from typing import List

from pymongo.results import InsertOneResult

from backend.MongoDBConnectorService import MongoDBConnectorService
from backend.model.mongo.Job import Job


class JobController:
    def __init__(self, mongo_db_connector_service: MongoDBConnectorService, collection_name='job'):
        self._mongo_db_connector_service = mongo_db_connector_service
        self._collection_name = collection_name

    def insert_one(self, job: Job) -> InsertOneResult:
        db = self._mongo_db_connector_service.get_db()
        job_dict = job.to_dict()
        job_dict["created_date"] = datetime.datetime.now()
        return db[self._collection_name].insert_one(job_dict)

    def find_all(self) -> List[Job]:
        db = self._mongo_db_connector_service.get_db()
        job_list = db[self._collection_name].find()
        if job_list is None:
            return []
        else:
            return list(map(Job.from_dict, job_list))
