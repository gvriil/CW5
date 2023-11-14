import os
from configparser import ConfigParser

DB_PARAMS = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'dbname': 'cw5',  # Добавьте вашу базу данных
    'port': os.getenv('DB_PORT'),
}