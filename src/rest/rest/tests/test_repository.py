import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
from bson import ObjectId
from rest.repositories import TodoRepository
from rest.exceptions import DatabaseError


class TestTodoRepository:

    @patch('rest.repositories.todo.MongoDBConnection')
    def test_find_all_returns_todos_sorted_descending(self, mock_db_conn):
        mock_collection = MagicMock()
        mock_db_conn.return_value.get_collection.return_value = mock_collection
        
        expected_todos = [
            {'_id': ObjectId(), 'text': 'Todo 1', 'created_at': datetime.utcnow()},
            {'_id': ObjectId(), 'text': 'Todo 2', 'created_at': datetime.utcnow()}
        ]
        mock_collection.find.return_value.sort.return_value = expected_todos
        
        repo = TodoRepository()
        result = repo.find_all()
        
        assert result == expected_todos
        mock_collection.find.return_value.sort.assert_called_once_with('_id', -1)

    @patch('rest.repositories.todo.MongoDBConnection')
    def test_find_all_returns_empty_list(self, mock_db_conn):
        mock_collection = MagicMock()
        mock_db_conn.return_value.get_collection.return_value = mock_collection
        mock_collection.find.return_value.sort.return_value = []
        
        repo = TodoRepository()
        result = repo.find_all()
        
        assert result == []

    @patch('rest.repositories.todo.MongoDBConnection')
    def test_find_all_raises_database_error_on_exception(self, mock_db_conn):
        mock_collection = MagicMock()
        mock_db_conn.return_value.get_collection.return_value = mock_collection
        mock_collection.find.side_effect = Exception('Connection failed')
        
        repo = TodoRepository()
        with pytest.raises(DatabaseError):
            repo.find_all()

    @patch('rest.repositories.todo.MongoDBConnection')
    def test_create_returns_todo_with_id(self, mock_db_conn):
        mock_collection = MagicMock()
        mock_db_conn.return_value.get_collection.return_value = mock_collection
        
        inserted_id = ObjectId()
        mock_collection.insert_one.return_value.inserted_id = inserted_id
        
        repo = TodoRepository()
        result = repo.create('New todo')
        
        assert result['text'] == 'New todo'
        assert result['_id'] == inserted_id
        assert 'created_at' in result

    @patch('rest.repositories.todo.MongoDBConnection')
    def test_create_raises_database_error_on_exception(self, mock_db_conn):
        mock_collection = MagicMock()
        mock_db_conn.return_value.get_collection.return_value = mock_collection
        mock_collection.insert_one.side_effect = Exception('Insert failed')
        
        repo = TodoRepository()
        with pytest.raises(DatabaseError):
            repo.create('New todo')

    @patch('rest.repositories.todo.MongoDBConnection')
    def test_delete_by_id_success(self, mock_db_conn):
        mock_collection = MagicMock()
        mock_db_conn.return_value.get_collection.return_value = mock_collection
        mock_collection.delete_one.return_value.deleted_count = 1
        
        repo = TodoRepository()
        result = repo.delete_by_id('507f1f77bcf86cd799439011')
        
        assert result is True

    @patch('rest.repositories.todo.MongoDBConnection')
    def test_delete_by_id_not_found(self, mock_db_conn):
        mock_collection = MagicMock()
        mock_db_conn.return_value.get_collection.return_value = mock_collection
        mock_collection.delete_one.return_value.deleted_count = 0
        
        repo = TodoRepository()
        result = repo.delete_by_id('507f1f77bcf86cd799439011')
        
        assert result is False

    @patch('rest.repositories.todo.MongoDBConnection')
    def test_delete_all_returns_count(self, mock_db_conn):
        mock_collection = MagicMock()
        mock_db_conn.return_value.get_collection.return_value = mock_collection
        mock_collection.delete_many.return_value.deleted_count = 5
        
        repo = TodoRepository()
        result = repo.delete_all()
        
        assert result == 5
        mock_collection.delete_many.assert_called_once_with({})
