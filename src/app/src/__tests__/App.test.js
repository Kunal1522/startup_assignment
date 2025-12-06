import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import App from '../App';
import { TodoAPI } from '../api/TodoAPI';

jest.mock('../api/TodoAPI');

describe('App', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should render app header', async () => {
    TodoAPI.getAll.mockResolvedValue({ todos: [] });

    render(<App />);

    expect(screen.getByText('Todo App')).toBeInTheDocument();
  });

  it('should render todo form', async () => {
    TodoAPI.getAll.mockResolvedValue({ todos: [] });

    render(<App />);

    expect(screen.getByPlaceholderText(/enter a new todo/i)).toBeInTheDocument();
  });

  it('should render todos from API', async () => {
    TodoAPI.getAll.mockResolvedValue({
      todos: [
        { id: '1', text: 'Test todo', created_at: '2025-12-05T10:00:00' }
      ]
    });

    render(<App />);

    await waitFor(() => {
      expect(screen.getByText('Test todo')).toBeInTheDocument();
    });
  });

  it('should render clear all button disabled when no todos', async () => {
    TodoAPI.getAll.mockResolvedValue({ todos: [] });

    render(<App />);

    await waitFor(() => {
      expect(screen.getByRole('button', { name: /clear all todos/i })).toBeDisabled();
    });
  });

  it('should render clear all button enabled when has todos', async () => {
    TodoAPI.getAll.mockResolvedValue({
      todos: [{ id: '1', text: 'Test', created_at: '2025-12-05T10:00:00' }]
    });

    render(<App />);

    await waitFor(() => {
      expect(screen.getByRole('button', { name: /clear all todos/i })).not.toBeDisabled();
    });
  });

  it('should show error message when fetch fails', async () => {
    TodoAPI.getAll.mockRejectedValue(new Error('Network error'));

    render(<App />);

    await waitFor(() => {
      expect(screen.getByText('Network error')).toBeInTheDocument();
    });
  });
});
