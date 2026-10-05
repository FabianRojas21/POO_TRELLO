from peewee import MySQLDatabase
from decouple import config

def conectar():
    database = MySQLDatabase(
        config('DB_NAME'),
        user=config('DB_USER'),
        password=config('DB_PASSWORD'),
        host=config('DB_HOST'),
        port=config('DB_PORT', cast=int),
        charset='utf8mb4'
    )
    return database