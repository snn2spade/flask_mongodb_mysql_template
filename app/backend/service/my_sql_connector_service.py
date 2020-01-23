import pandas as pd
from mysql.connector import connect, MySQLConnection, Error as MySQLConnectorError

from app.config_loader import AppConfig


class MySQLConnectorService:

    @staticmethod
    def init_connection(username: str = AppConfig().config["DATABASE"]["MYSQL"]["DB_USERNAME"],
                        password: str = AppConfig().config["DATABASE"]["MYSQL"]["DB_PASSWORD"],
                        host: str = AppConfig().config["DATABASE"]["MYSQL"]["DB_HOST"],
                        db_name: str = AppConfig().config["DATABASE"]["MYSQL"]["DB_NAME"]):
        try:
            return connect(user=username, password=password, host=host, database=db_name)
        except MySQLConnectorError as err:
            print(err)

    @staticmethod
    def execute_query(statement: str, connection: MySQLConnection):
        return pd.read_sql(statement, con=connection)
