import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import TodoList from '../components/TodoList';

describe('TodoList', () => {
  const mockOnDelete = jest.fn();

  beforeEach(() => {
    mockOnDelete.mockClear();
  });

  it('should render loading state', () => {
    render(<TodoList todos={[]} loading={true} onDelete={mockOnDelete} />);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  it('should render empty message when no todos', () => {
    render(<TodoList todos={[]} loading={false} onDelete={mockOnDelete} />);
    expect(screen.getByText(/no todos yet/i)).toBeInTheDocument();
  });

  it('should render todos', () => {
    const todos = [
      { id: '1', text: 'First todo', created_at: '2025-12-05T10:00:00' },
      { id: '2', text: 'Second todo', created_at: '2025-12-05T11:00:00' }
    ];

    render(<TodoList todos={todos} loading={false} onDelete={mockOnDelete} />);

    expect(screen.getByText('First todo')).toBeInTheDocument();
    expect(screen.getByText('Second todo')).toBeInTheDocument();
  });

  it('should call onDelete when delete button is clicked', () => {
    const todos = [
      { id: '1', text: 'Test todo', created_at: '2025-12-05T10:00:00' }
    ];

    render(<TodoList todos={todos} loading={false} onDelete={mockOnDelete} />);

    const deleteButton = screen.getByTitle('Delete');
    fireEvent.click(deleteButton);

    expect(mockOnDelete).toHaveBeenCalledWith('1');
  });

  it('should render date for each todo', () => {
    const todos = [
      { id: '1', text: 'Test todo', created_at: '2025-12-05T10:00:00' }
    ];

    render(<TodoList todos={todos} loading={false} onDelete={mockOnDelete} />);

    expect(screen.getByText('12/5/2025')).toBeInTheDocument();
  });
});
