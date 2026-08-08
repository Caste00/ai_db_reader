from utils.config import config
from database.sqlalchemy_connector import SQLAlchemyConnector
from database.database_connector_abc import DatabaseConnector


def get_connector() -> DatabaseConnector:
    return SQLAlchemyConnector(config.target_database)