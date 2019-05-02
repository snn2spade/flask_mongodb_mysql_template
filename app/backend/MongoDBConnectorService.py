from pymongo import MongoClient

from ConfigLoader import AppConfig


class MongoDBConnectorService:
    db = None

    @staticmethod
    def get_db(username=AppConfig().config["MONGO"]["USERNAME"], password=AppConfig().config["MONGO"]["PASSWORD"],
               host=AppConfig().config["MONGO"]["HOST"],
               db_name=AppConfig().config["MONGO"]["DB_NAME"],
               auth_db_name=AppConfig().config["MONGO"]["AUTH_DB_NAME"]):
        if MongoDBConnectorService.db is None:
            if auth_db_name is not None:
                MongoDBConnectorService.db = MongoClient(host, 27017, username=username, password=password, authSource=auth_db_name)[db_name]
            else:
                MongoDBConnectorService.db = MongoClient(host, 27017, username=username, password=password)[db_name]

        return MongoDBConnectorService.db
