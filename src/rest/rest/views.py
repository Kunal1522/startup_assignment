from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.exceptions import ParseError

from .core import AppLogger
from .services import TodoService
from .exceptions import AppException


class TodoListView(APIView):
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._logger = AppLogger('view.todo')
        self._service = TodoService()

    def get(self, request):
        try:
            self._logger.info('GET /todos/ request received')
            data = self._service.get_all()
            return Response(data, status=status.HTTP_200_OK)
        except AppException as e:
            self._logger.warning('Request failed', context={'error': e.message})
            return Response(e.to_dict(), status=e.status_code)
        except Exception as e:
            self._logger.error('Unexpected error in GET /todos/', exception=e)
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        try:
            self._logger.info('POST /todos/ request received')
            # Handle both JSON and form data, catch parse errors
            try:
                text = request.data.get('text') if request.data else None
            except ParseError:
                text = None
            todo = self._service.create(text)
            self._logger.info('Todo created', context={'id': todo['id']})
            return Response(todo, status=status.HTTP_201_CREATED)
        except AppException as e:
            self._logger.warning('Request failed', context={'error': e.message})
            return Response(e.to_dict(), status=e.status_code)
        except ParseError as e:
            self._logger.warning('Parse error in POST', context={'error': str(e)})
            return Response(
                {'error': 'Invalid request body', 'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            self._logger.error('Unexpected error in POST /todos/', exception=e)
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request):
        try:
            self._logger.info('DELETE /todos/ request received (clear all)')
            deleted_count = self._service.delete_all()
            return Response(
                {'message': 'All todos deleted', 'deleted_count': deleted_count},
                status=status.HTTP_200_OK
            )
        except AppException as e:
            self._logger.warning('Request failed', context={'error': e.message})
            return Response(e.to_dict(), status=e.status_code)
        except Exception as e:
            self._logger.error('Unexpected error in DELETE /todos/', exception=e)
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TodoDetailView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._logger = AppLogger('view.todo.detail')
        self._service = TodoService()

    def delete(self, request, todo_id):
        try:
            self._logger.info('DELETE /todos/{id}/ request received', context={'id': todo_id})
            deleted = self._service.delete(todo_id)
            if not deleted:
                return Response(
                    {'error': 'Todo not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AppException as e:
            self._logger.warning('Request failed', context={'error': e.message})
            return Response(e.to_dict(), status=e.status_code)
        except Exception as e:
            self._logger.error('Unexpected error in DELETE /todos/{id}/', exception=e)
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
