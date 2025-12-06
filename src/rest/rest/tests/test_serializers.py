import pytest
from datetime import datetime
from bson import ObjectId
from rest.serializers import TodoSerializer


class TestTodoSerializer:

    def test_serialize_single_todo(self):
        todo = {
            '_id': ObjectId('507f1f77bcf86cd799439011'),
            'text': 'Test todo',
            'created_at': datetime(2025, 12, 5, 10, 30, 0)
        }
        result = TodoSerializer.serialize(todo)
        
        assert result['id'] == '507f1f77bcf86cd799439011'
        assert result['text'] == 'Test todo'
        assert result['created_at'] == '2025-12-05T10:30:00'

    def test_serialize_todo_without_created_at(self):
        todo = {
            '_id': ObjectId('507f1f77bcf86cd799439011'),
            'text': 'Test todo'
        }
        result = TodoSerializer.serialize(todo)
        
        assert result['id'] == '507f1f77bcf86cd799439011'
        assert result['text'] == 'Test todo'
        assert result['created_at'] is None

    def test_serialize_todo_with_empty_text(self):
        todo = {
            '_id': ObjectId(),
            'text': '',
            'created_at': datetime.utcnow()
        }
        result = TodoSerializer.serialize(todo)
        assert result['text'] == ''

    def test_serialize_many_todos(self):
        todos = [
            {
                '_id': ObjectId('507f1f77bcf86cd799439011'),
                'text': 'First',
                'created_at': datetime(2025, 12, 5, 10, 0, 0)
            },
            {
                '_id': ObjectId('507f1f77bcf86cd799439012'),
                'text': 'Second',
                'created_at': datetime(2025, 12, 5, 11, 0, 0)
            }
        ]
        result = TodoSerializer.serialize_many(todos)
        
        assert len(result) == 2
        assert result[0]['text'] == 'First'
        assert result[1]['text'] == 'Second'

    def test_serialize_empty_list(self):
        result = TodoSerializer.serialize_many([])
        assert result == []
