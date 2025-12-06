import pytest
from unittest.mock import MagicMock, patch
from rest_framework.test import APIRequestFactory
from rest_framework import status
from datetime import datetime
from bson import ObjectId

from rest.views import TodoListView, TodoDetailView
from rest.exceptions import ValidationError, DatabaseError


class TestTodoListView:

    def setup_method(self):
        self.factory = APIRequestFactory()

    @patch('rest.views.TodoService')
    def test_get_todos_success(self, mock_service_class):
        mock_service = MagicMock()
        mock_service_class.return_value = mock_service
        mock_service.get_all.return_value = {
            'todos': [
                {'id': '1', 'text': 'Todo 1', 'created_at': '2025-12-05T10:00:00'},
                {'id': '2', 'text': 'Todo 2', 'created_at': '2025-12-05T11:00:00'}
            ],
            'count': 2
        }

        request = self.factory.get('/todos/')
        view = TodoListView.as_view()
        response = view(request)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 2
        assert len(response.data['todos']) == 2

    @patch('rest.views.TodoService')
    def test_get_todos_empty(self, mock_service_class):
        mock_service = MagicMock()
        mock_service_class.return_value = mock_service
        mock_service.get_all.return_value = {'todos': [], 'count': 0}

        request = self.factory.get('/todos/')
        view = TodoListView.as_view()
        response = view(request)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 0

    @patch('rest.views.TodoService')
    def test_get_todos_database_error(self, mock_service_class):
        mock_service = MagicMock()
        mock_service_class.return_value = mock_service
        mock_service.get_all.side_effect = DatabaseError('DB connection failed')

        request = self.factory.get('/todos/')
        view = TodoListView.as_view()
        response = view(request)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    @patch('rest.views.TodoService')
    def test_post_todo_success(self, mock_service_class):
        mock_service = MagicMock()
        mock_service_class.return_value = mock_service
        mock_service.create.return_value = {
            'id': '507f1f77bcf86cd799439011',
            'text': 'New todo',
            'created_at': '2025-12-05T10:00:00'
        }

        request = self.factory.post('/todos/', {'text': 'New todo'}, format='json')
        view = TodoListView.as_view()
        response = view(request)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['text'] == 'New todo'

    @patch('rest.views.TodoService')
    def test_post_todo_validation_error(self, mock_service_class):
        mock_service = MagicMock()
        mock_service_class.return_value = mock_service
        mock_service.create.side_effect = ValidationError('Text is required')

        request = self.factory.post('/todos/', {'text': ''}, format='json')
        view = TodoListView.as_view()
        response = view(request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('rest.views.TodoService')
    def test_post_todo_without_text(self, mock_service_class):
        mock_service = MagicMock()
        mock_service_class.return_value = mock_service
        mock_service.create.side_effect = ValidationError('Text is required')

        request = self.factory.post('/todos/', {}, format='json')
        view = TodoListView.as_view()
        response = view(request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('rest.views.TodoService')
    def test_delete_all_todos_success(self, mock_service_class):
        mock_service = MagicMock()
        mock_service_class.return_value = mock_service
        mock_service.delete_all.return_value = 5

        request = self.factory.delete('/todos/')
        view = TodoListView.as_view()
        response = view(request)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['deleted_count'] == 5


class TestTodoDetailView:

    def setup_method(self):
        self.factory = APIRequestFactory()

    @patch('rest.views.TodoService')
    def test_delete_todo_success(self, mock_service_class):
        mock_service = MagicMock()
        mock_service_class.return_value = mock_service
        mock_service.delete.return_value = True

        request = self.factory.delete('/todos/507f1f77bcf86cd799439011/')
        view = TodoDetailView.as_view()
        response = view(request, todo_id='507f1f77bcf86cd799439011')

        assert response.status_code == status.HTTP_204_NO_CONTENT

    @patch('rest.views.TodoService')
    def test_delete_todo_not_found(self, mock_service_class):
        mock_service = MagicMock()
        mock_service_class.return_value = mock_service
        mock_service.delete.return_value = False

        request = self.factory.delete('/todos/507f1f77bcf86cd799439011/')
        view = TodoDetailView.as_view()
        response = view(request, todo_id='507f1f77bcf86cd799439011')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch('rest.views.TodoService')
    def test_delete_todo_validation_error(self, mock_service_class):
        mock_service = MagicMock()
        mock_service_class.return_value = mock_service
        mock_service.delete.side_effect = ValidationError('Invalid ID')

        request = self.factory.delete('/todos/invalid/')
        view = TodoDetailView.as_view()
        response = view(request, todo_id='invalid')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
