import mysql.connector
from src.config import DevelopmentConfig

def get_mysql_connection():
    config = {
        "host": DevelopmentConfig.MYSQL_HOST,
        "user": DevelopmentConfig.MYSQL_USER,
        "password": DevelopmentConfig.MYSQL_PASSWORD,
        "database": DevelopmentConfig.MYSQL_DB
    }
    return mysql.connector.connect(**config)