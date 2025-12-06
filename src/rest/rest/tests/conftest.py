import pytest
from unittest.mock import MagicMock, patch
from bson import ObjectId
from datetime import datetime


@pytest.fixture
def mock_mongo_collection():
    with patch('rest.core.database.MongoClient') as mock_client:
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_client.return_value.__getitem__.return_value = mock_db
        mock_db.__getitem__.return_value = mock_collection
        mock_db.todos = mock_collection
        yield mock_collection


@pytest.fixture
def sample_todo():
    return {
        '_id': ObjectId(),
        'text': 'Test todo item',
        'created_at': datetime.utcnow()
    }


@pytest.fixture
def sample_todos():
    return [
        {
            '_id': ObjectId(),
            'text': 'First todo',
            'created_at': datetime.utcnow()
        },
        {
            '_id': ObjectId(),
            'text': 'Second todo',
            'created_at': datetime.utcnow()
        }
    ]


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()
