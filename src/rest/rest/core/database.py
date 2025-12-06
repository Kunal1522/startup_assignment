from pymongo import MongoClient
from typing import Optional
import os

from .logger import AppLogger


class MongoDBConnection:
    _instance: Optional['MongoDBConnection'] = None
    _logger = AppLogger('database')

    def __new__(cls) -> 'MongoDBConnection':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self) -> None:
        host = os.environ.get('MONGO_HOST', 'localhost')
        port = os.environ.get('MONGO_PORT', '27017')
        connection_string = f'mongodb://{host}:{port}'
        
        self._logger.info('Connecting to MongoDB', {'host': host, 'port': port})
        
        try:
            self.client = MongoClient(connection_string)
            self.db = self.client['test_db']
            self._logger.info('MongoDB connection established')
        except Exception as e:
            self._logger.critical('Failed to connect to MongoDB', exception=e)
            raise

    def get_collection(self, name: str):
        return self.db[name]
