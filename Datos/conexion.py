from peewee import *
from decouple import config
def conectar():
    database = MySQLDatabase(config('trello_db', **{
        'charset': 'utf8mb4', 
        'host': config('DB_HOST'), 
        'port': config('DB_PORT'), 
        'user': config('DB_USER'),
        'password': config('DB_PASSWORD')}))
    return database