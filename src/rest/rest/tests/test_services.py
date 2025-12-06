import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
from bson import ObjectId
from rest.services import TodoService
from rest.exceptions import ValidationError, DatabaseError


class TestTodoService:

    @patch('rest.services.todo.TodoRepository')
    def test_get_all_returns_serialized_todos(self, mock_repo_class):
        mock_repo = MagicMock()
        mock_repo_class.return_value = mock_repo
        
        mock_repo.find_all.return_value = [
            {'_id': ObjectId(), 'text': 'Todo 1', 'created_at': datetime.utcnow()},
            {'_id': ObjectId(), 'text': 'Todo 2', 'created_at': datetime.utcnow()}
        ]
        
        service = TodoService()
        result = service.get_all()
        
        assert 'todos' in result
        assert 'count' in result
        assert result['count'] == 2
        assert len(result['todos']) == 2

    @patch('rest.services.todo.TodoRepository')
    def test_get_all_empty_list(self, mock_repo_class):
        mock_repo = MagicMock()
        mock_repo_class.return_value = mock_repo
        mock_repo.find_all.return_value = []
        
        service = TodoService()
        result = service.get_all()
        
        assert result['todos'] == []
        assert result['count'] == 0

    @patch('rest.services.todo.TodoRepository')
    def test_create_success(self, mock_repo_class):
        mock_repo = MagicMock()
        mock_repo_class.return_value = mock_repo
        
        created_todo = {
            '_id': ObjectId(),
            'text': 'New todo',
            'created_at': datetime.utcnow()
        }
        mock_repo.create.return_value = created_todo
        
        service = TodoService()
        result = service.create('New todo')
        
        assert result['text'] == 'New todo'
        assert 'id' in result

    @patch('rest.services.todo.TodoRepository')
    def test_create_with_invalid_text_raises_error(self, mock_repo_class):
        service = TodoService()
        
        with pytest.raises(ValidationError):
            service.create(None)
        
        with pytest.raises(ValidationError):
            service.create('')

    @patch('rest.services.todo.TodoRepository')
    def test_delete_success(self, mock_repo_class):
        mock_repo = MagicMock()
        mock_repo_class.return_value = mock_repo
        mock_repo.delete_by_id.return_value = True
        
        service = TodoService()
        result = service.delete('507f1f77bcf86cd799439011')
        
        assert result is True

    @patch('rest.services.todo.TodoRepository')
    def test_delete_not_found(self, mock_repo_class):
        mock_repo = MagicMock()
        mock_repo_class.return_value = mock_repo
        mock_repo.delete_by_id.return_value = False
        
        service = TodoService()
        result = service.delete('507f1f77bcf86cd799439011')
        
        assert result is False

    @patch('rest.services.todo.TodoRepository')
    def test_delete_with_empty_id_raises_error(self, mock_repo_class):
        service = TodoService()
        
        with pytest.raises(ValidationError):
            service.delete('')
        
        with pytest.raises(ValidationError):
            service.delete(None)

    @patch('rest.services.todo.TodoRepository')
    def test_delete_all_returns_count(self, mock_repo_class):
        mock_repo = MagicMock()
        mock_repo_class.return_value = mock_repo
        mock_repo.delete_all.return_value = 10
        
        service = TodoService()
        result = service.delete_all()
        
        assert result == 10
