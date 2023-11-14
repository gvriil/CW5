import os
from configparser import ConfigParser

DB_PARAMS = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', '12345'),
    'dbname': 'cw5',  # Добавьте вашу базу данных
    'port': os.getenv('DB_PORT', '5433'),
}