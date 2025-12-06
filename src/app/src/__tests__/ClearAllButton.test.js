import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import ClearAllButton from '../components/ClearAllButton';

describe('ClearAllButton', () => {
  const mockOnClearAll = jest.fn();

  beforeEach(() => {
    mockOnClearAll.mockClear();
    mockOnClearAll.mockResolvedValue(true);
  });

  it('should render clear all button', () => {
    render(<ClearAllButton onClearAll={mockOnClearAll} disabled={false} />);
    expect(screen.getByRole('button', { name: /clear all todos/i })).toBeInTheDocument();
  });

  it('should be disabled when disabled prop is true', () => {
    render(<ClearAllButton onClearAll={mockOnClearAll} disabled={true} />);
    expect(screen.getByRole('button', { name: /clear all todos/i })).toBeDisabled();
  });

  it('should show confirmation dialog when clicked', () => {
    render(<ClearAllButton onClearAll={mockOnClearAll} disabled={false} />);
    
    const button = screen.getByRole('button', { name: /clear all todos/i });
    fireEvent.click(button);

    expect(screen.getByText(/are you sure/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /yes/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /no/i })).toBeInTheDocument();
  });

  it('should call onClearAll when confirmed', async () => {
    render(<ClearAllButton onClearAll={mockOnClearAll} disabled={false} />);
    
    const button = screen.getByRole('button', { name: /clear all todos/i });
    fireEvent.click(button);

    const yesButton = screen.getByRole('button', { name: /yes/i });
    fireEvent.click(yesButton);

    await waitFor(() => {
      expect(mockOnClearAll).toHaveBeenCalled();
    });
  });

  it('should close dialog when cancelled', () => {
    render(<ClearAllButton onClearAll={mockOnClearAll} disabled={false} />);
    
    const button = screen.getByRole('button', { name: /clear all todos/i });
    fireEvent.click(button);

    const noButton = screen.getByRole('button', { name: /no/i });
    fireEvent.click(noButton);

    expect(screen.queryByText(/are you sure/i)).not.toBeInTheDocument();
    expect(mockOnClearAll).not.toHaveBeenCalled();
  });

  it('should close dialog after confirmation', async () => {
    render(<ClearAllButton onClearAll={mockOnClearAll} disabled={false} />);
    
    const button = screen.getByRole('button', { name: /clear all todos/i });
    fireEvent.click(button);

    const yesButton = screen.getByRole('button', { name: /yes/i });
    fireEvent.click(yesButton);

    await waitFor(() => {
      expect(screen.queryByText(/are you sure/i)).not.toBeInTheDocument();
    });
  });
});
