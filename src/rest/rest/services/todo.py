from typing import Dict, Any

from ..core import AppLogger
from ..repositories import TodoRepository
from ..serializers import TodoSerializer
from ..validators import TodoValidator


class TodoService:
    def __init__(self):
        self._logger = AppLogger('service.todo')
        self._repository = TodoRepository()

    def get_all(self) -> Dict[str, Any]:
        self._logger.info('Getting all todos')
        todos = self._repository.find_all()
        serialized = TodoSerializer.serialize_many(todos)
        return {
            'todos': serialized,
            'count': len(serialized)
        }

    def create(self, text: any) -> Dict[str, Any]:
        self._logger.info('Creating new todo')
        validated_text = TodoValidator.validate_text(text)
        todo = self._repository.create(validated_text)
        return TodoSerializer.serialize(todo)

    def delete(self, todo_id: str) -> bool:
        self._logger.info('Deleting todo', context={'id': todo_id})
        if not todo_id:
            from ..exceptions import ValidationError
            raise ValidationError('Todo ID is required')
        return self._repository.delete_by_id(todo_id)

    def delete_all(self) -> int:
        self._logger.info('Deleting all todos')
        return self._repository.delete_all()
