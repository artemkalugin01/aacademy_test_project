import psycopg2
import os


def connect_db():
    """
    вспомогательный метод для подключения к БД
    переменные читаются из файла окружения
    :return:
    """
    return psycopg2.connect(
        database=os.getenv('DATABASE'),
        user=os.getenv('USER'),
        password=os.getenv('PASSWORD'),
        host=os.getenv('HOST'), port=os.getenv('PORT')
    )
