from typing import List, Dict, Any
from datetime import datetime


class TodoSerializer:
    @staticmethod
    def serialize(todo: dict) -> Dict[str, Any]:
        created_at = todo.get('created_at')
        if isinstance(created_at, datetime):
            created_at = created_at.isoformat()
        
        return {
            'id': str(todo['_id']),
            'text': todo.get('text', ''),
            'created_at': created_at
        }

    @classmethod
    def serialize_many(cls, todos: List[dict]) -> List[Dict[str, Any]]:
        return [cls.serialize(todo) for todo in todos]
