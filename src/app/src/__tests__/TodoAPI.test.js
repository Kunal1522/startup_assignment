import { TodoAPI, ApiError } from '../api/TodoAPI';

global.fetch = jest.fn();

describe('TodoAPI', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  describe('getAll', () => {
    it('should fetch all todos successfully', async () => {
      const mockTodos = {
        todos: [
          { id: '1', text: 'Todo 1', created_at: '2025-12-05T10:00:00' },
          { id: '2', text: 'Todo 2', created_at: '2025-12-05T11:00:00' }
        ],
        count: 2
      };

      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockTodos
      });

      const result = await TodoAPI.getAll();

      expect(fetch).toHaveBeenCalledWith('/todos/');
      expect(result).toEqual(mockTodos);
    });

    it('should throw ApiError on fetch failure', async () => {
      fetch.mockResolvedValueOnce({
        ok: false,
        status: 500
      });

      await expect(TodoAPI.getAll()).rejects.toThrow(ApiError);
    });
  });

  describe('create', () => {
    it('should create a todo successfully', async () => {
      const newTodo = { id: '1', text: 'New todo', created_at: '2025-12-05T10:00:00' };

      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => newTodo
      });

      const result = await TodoAPI.create('New todo');

      expect(fetch).toHaveBeenCalledWith('/todos/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: 'New todo' })
      });
      expect(result).toEqual(newTodo);
    });

    it('should throw ApiError with message on validation error', async () => {
      fetch.mockResolvedValueOnce({
        ok: false,
        status: 400,
        json: async () => ({ error: 'Text is required' })
      });

      await expect(TodoAPI.create('')).rejects.toThrow('Text is required');
    });
  });

  describe('deleteOne', () => {
    it('should delete a todo successfully', async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        status: 204
      });

      const result = await TodoAPI.deleteOne('123');

      expect(fetch).toHaveBeenCalledWith('/todos/123/', {
        method: 'DELETE'
      });
      expect(result).toBe(true);
    });

    it('should throw ApiError on delete failure', async () => {
      fetch.mockResolvedValueOnce({
        ok: false,
        status: 500
      });

      await expect(TodoAPI.deleteOne('123')).rejects.toThrow(ApiError);
    });
  });

  describe('deleteAll', () => {
    it('should delete all todos successfully', async () => {
      const response = { message: 'All todos deleted', deleted_count: 5 };

      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => response
      });

      const result = await TodoAPI.deleteAll();

      expect(fetch).toHaveBeenCalledWith('/todos/', {
        method: 'DELETE'
      });
      expect(result).toEqual(response);
    });
  });
});
