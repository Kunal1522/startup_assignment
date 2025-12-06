from typing import List, Dict, Any
from datetime import datetime

from ..core import MongoDBConnection, AppLogger
from ..exceptions import DatabaseError


class TodoRepository:
    COLLECTION_NAME = 'todos'

    def __init__(self):
        self._logger = AppLogger('repository.todo')
        self._collection = MongoDBConnection().get_collection(self.COLLECTION_NAME)

    def find_all(self) -> List[Dict[str, Any]]:
        try:
            self._logger.debug('Fetching all todos')
            todos = list(self._collection.find().sort('_id', -1))
            self._logger.info('Todos fetched successfully', {'count': len(todos)})
            return todos
        except Exception as e:
            self._logger.error('Failed to fetch todos', exception=e)
            raise DatabaseError('Failed to retrieve todos')

    def delete_by_id(self, todo_id: str) -> bool:
        try:
            from bson import ObjectId
            self._logger.debug('Deleting todo', {'id': todo_id})
            result = self._collection.delete_one({'_id': ObjectId(todo_id)})
            if result.deleted_count == 0:
                self._logger.warning('Todo not found for deletion', {'id': todo_id})
                return False
            self._logger.info('Todo deleted successfully', {'id': todo_id})
            return True
        except Exception as e:
            self._logger.error('Failed to delete todo', exception=e)
            raise DatabaseError('Failed to delete todo')

    def delete_all(self) -> int:
        try:
            self._logger.debug('Deleting all todos')
            result = self._collection.delete_many({})
            self._logger.info('All todos deleted', {'count': result.deleted_count})
            return result.deleted_count
        except Exception as e:
            self._logger.error('Failed to delete all todos', exception=e)
            raise DatabaseError('Failed to delete all todos')

    def create(self, text: str) -> Dict[str, Any]:
        try:
            todo_data = {
                'text': text,
                'created_at': datetime.utcnow()
            }
            self._logger.debug('Creating todo', {'text': text[:50]})
            result = self._collection.insert_one(todo_data)
            todo_data['_id'] = result.inserted_id
            self._logger.info('Todo created successfully', {'id': str(result.inserted_id)})
            return todo_data
        except Exception as e:
            self._logger.error('Failed to create todo', exception=e)
            raise DatabaseError('Failed to create todo')
