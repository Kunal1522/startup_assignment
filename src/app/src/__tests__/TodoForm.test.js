import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import TodoForm from '../components/TodoForm';

describe('TodoForm', () => {
  const mockOnSubmit = jest.fn();

  beforeEach(() => {
    mockOnSubmit.mockClear();
    mockOnSubmit.mockResolvedValue(true);
  });

  it('should render input and button', () => {
    render(<TodoForm onSubmit={mockOnSubmit} />);

    expect(screen.getByPlaceholderText(/enter a new todo/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /add todo/i })).toBeInTheDocument();
  });

  it('should update input value on change', async () => {
    render(<TodoForm onSubmit={mockOnSubmit} />);

    const input = screen.getByPlaceholderText(/enter a new todo/i);
    await userEvent.type(input, 'New todo');

    expect(input).toHaveValue('New todo');
  });

  it('should call onSubmit with trimmed text', async () => {
    render(<TodoForm onSubmit={mockOnSubmit} />);

    const input = screen.getByPlaceholderText(/enter a new todo/i);
    const button = screen.getByRole('button', { name: /add todo/i });

    await userEvent.type(input, '  New todo  ');
    fireEvent.click(button);

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith('New todo');
    });
  });

  it('should clear input after successful submit', async () => {
    render(<TodoForm onSubmit={mockOnSubmit} />);

    const input = screen.getByPlaceholderText(/enter a new todo/i);
    const button = screen.getByRole('button', { name: /add todo/i });

    await userEvent.type(input, 'New todo');
    fireEvent.click(button);

    await waitFor(() => {
      expect(input).toHaveValue('');
    });
  });

  it('should not submit empty text', async () => {
    render(<TodoForm onSubmit={mockOnSubmit} />);

    const button = screen.getByRole('button', { name: /add todo/i });
    fireEvent.click(button);

    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  it('should not submit whitespace only', async () => {
    render(<TodoForm onSubmit={mockOnSubmit} />);

    const input = screen.getByPlaceholderText(/enter a new todo/i);
    const button = screen.getByRole('button', { name: /add todo/i });

    await userEvent.type(input, '   ');
    fireEvent.click(button);

    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  it('should not clear input on failed submit', async () => {
    mockOnSubmit.mockResolvedValue(false);
    render(<TodoForm onSubmit={mockOnSubmit} />);

    const input = screen.getByPlaceholderText(/enter a new todo/i);
    const button = screen.getByRole('button', { name: /add todo/i });

    await userEvent.type(input, 'New todo');
    fireEvent.click(button);

    await waitFor(() => {
      expect(input).toHaveValue('New todo');
    });
  });
});
