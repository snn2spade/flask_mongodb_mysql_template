from pymongo import MongoClient
from app.config_loader import AppConfig


class MongoDBConnectorService:
    db = None

    @staticmethod
    def get_db(username: str = AppConfig().config["DATABASE"]["MONGO"]["USERNAME"],
               password: str = AppConfig().config["DATABASE"]["MONGO"]["PASSWORD"],
               host: str = AppConfig().config["DATABASE"]["MONGO"]["HOST"],
               db_name: str = AppConfig().config["DATABASE"]["MONGO"]["DB_NAME"],
               auth_db_name: str = AppConfig().config["DATABASE"]["MONGO"]["AUTH_DB_NAME"]):
        if MongoDBConnectorService.db is None:
            if auth_db_name is not None:
                MongoDBConnectorService.db = MongoClient(host, 27017, username=username, password=password,
                                                         authSource=auth_db_name)[db_name]
            else:
                MongoDBConnectorService.db = MongoClient(host, 27017, username=username, password=password)[db_name]

        return MongoDBConnectorService.db
