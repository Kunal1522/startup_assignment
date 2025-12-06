from typing import Optional
from rest_framework import status


class AppException(Exception):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_message: str = 'An unexpected error occurred'

    def __init__(self, message: Optional[str] = None, details: Optional[dict] = None):
        self.message = message or self.default_message
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> dict:
        response = {'error': self.message}
        if self.details:
            response['details'] = self.details
        return response


class ValidationError(AppException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = 'Validation failed'


class NotFoundError(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    default_message = 'Resource not found'


class DatabaseError(AppException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_message = 'Database operation failed'
