const API_URL = process.env.REACT_APP_API_URL || '';

class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

class TodoAPI {
  static async getAll() {
    const res = await fetch(`${API_URL}/todos/`);
    if (!res.ok) throw new ApiError('Failed to fetch todos', res.status);
    return res.json();
  }

  static async create(text) {
    const res = await fetch(`${API_URL}/todos/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
    const data = await res.json();
    if (!res.ok) throw new ApiError(data.error || 'Failed to create todo', res.status);
    return data;
  }

  static async deleteOne(id) {
    const res = await fetch(`${API_URL}/todos/${id}/`, {
      method: 'DELETE'
    });
    if (!res.ok && res.status !== 204) {
      throw new ApiError('Failed to delete todo', res.status);
    }
    return true;
  }

  static async deleteAll() {
    const res = await fetch(`${API_URL}/todos/`, {
      method: 'DELETE'
    });
    if (!res.ok) throw new ApiError('Failed to delete all todos', res.status);
    return res.json();
  }
}

export { TodoAPI, ApiError };
export default TodoAPI;
