import os
from pathlib import Path

from pymongo.errors import DuplicateKeyError
from bson.json_util import loads as bson_loads

from app.backend.service.mongo_db_connector_service import MongoDBConnectorService

print("---------- START MIGRATION ----------")
mongo_db_connector_service = MongoDBConnectorService()
cur_path = os.path.abspath(os.path.dirname(__file__))
target_path = os.path.join(Path(cur_path), "migration/")
total_inserted_doc = 0
for folder in os.listdir(target_path):
    target_folder = os.path.join(target_path, folder)
    inserted_doc = 0
    for file in os.listdir(target_folder):
        target_file = os.path.join(target_folder, file)
        with open(target_file, "r") as file:
            doc = bson_loads(file.read())
            try:
                mongo_db_connector_service.get_db()[folder].insert_one(doc)
                inserted_doc += 1
                total_inserted_doc += 1
            except DuplicateKeyError:
                continue
    print(f'Collection "{folder}" inserted {inserted_doc} documents')
if total_inserted_doc == 0:
    print("Migration completed -> No document have been inserted")
else:
    print("Migration completed: -> total doc inserted : {}".format(total_inserted_doc))
