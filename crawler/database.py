""":mod:`crawler.database` ---  MongoDB Manager
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import logging

from pymongo import MongoClient
import psycopg2 as pg2


from .config import crawler_config_mongo as crawler_config
from .config import crawler_config_postgres as crawler_config_postgres


logger = logging.getLogger(__name__)


class PostgresDB:
    def __init__(self, db: str):
        self.db_name = 'crawler'
        self.db_id = 'postgres'
        self.db_pw = 'qudtlstz1'
        self.db_host = 'localhost'
        self.cur = None

    def connect(self):
        try:
            conn = pg2.connect('host=localhost user=postgres dbname=test password=qudtlstz1')
        except:
            conn = pg2.connect('host=localhost user=postgres password=qudtlstz1')

            conn.autocommit = True
            cur = conn.cursor()

            cur.execute('create database test')
            cur.execute('SELECT version()')

            cur.execute('create table archive (id serial PRIMARY KEY, type varchar,  link varchar , count integer ,\
                         title varchar , date timestamp , article text)')

            conn.close()

            conn = pg2.connect('host=localhost user=postgres dbname=test password=qudtlstz1')

        conn.autocommit = True
        self.cur = conn.cursor()

    def query(self, document: str):
        self.cur.execute()





class MongoDB:
    def __init__(self, db: str):
        db_config = crawler_config.db_config
        client = MongoClient(host=db_config['url'],
                             serverSelectionTimeoutMS=3)
        self.collection = client[db]

    def query(self, document: str):
        return self.collection[document]

    def insert(self, document: str, *, data: dict):
        return self.collection[document] \
            .insert(data)

    def update(self, document: str, *, c, data: dict):
        return self.collection[document] \
            .update({'_id': c['_id']}, {'$set': data})
