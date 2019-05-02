import mysql.connector
import pandas as pd

from ConfigLoader import AppConfig


class MySQLConnectorService:

    @staticmethod
    def init_connection(username=AppConfig().config["MYSQL"]["DB_USERNAME"], password=AppConfig().config["MYSQL"]["DB_PASSWORD"],
                        host=AppConfig().config["MYSQL"]["DB_HOST"],
                        db_name=AppConfig().config["MYSQL"]["DB_NAME"]):
        try:
            return mysql.connector.connect(user=username, password=password, host=host, database=db_name)
        except mysql.connector.Error as err:
            print(err)

    @staticmethod
    def execute_query(statement, connection):
        return pd.read_sql(statement, con=connection)
