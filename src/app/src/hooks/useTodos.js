import { useState, useEffect, useCallback } from 'react';
import { TodoAPI } from '../api/TodoAPI';

function useTodos() {
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchTodos = useCallback(async () => {
    try {
      setLoading(true);
      const data = await TodoAPI.getAll();
      setTodos(data.todos || []);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  const addTodo = useCallback(async (text) => {
    try {
      await TodoAPI.create(text);
      await fetchTodos();
      return true;
    } catch (err) {
      setError(err.message);
      return false;
    }
  }, [fetchTodos]);

  const deleteTodo = useCallback(async (id) => {
    try {
      await TodoAPI.deleteOne(id);
      await fetchTodos();
      return true;
    } catch (err) {
      setError(err.message);
      return false;
    }
  }, [fetchTodos]);

  const deleteAllTodos = useCallback(async () => {
    try {
      await TodoAPI.deleteAll();
      await fetchTodos();
      return true;
    } catch (err) {
      setError(err.message);
      return false;
    }
  }, [fetchTodos]);

  const clearError = useCallback(() => setError(null), []);

  useEffect(() => { fetchTodos(); }, [fetchTodos]);

  return { todos, loading, error, addTodo, deleteTodo, deleteAllTodos, clearError };
}

export default useTodos;
