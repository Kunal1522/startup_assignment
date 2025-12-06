import React from 'react';
import useTodos from './hooks/useTodos';
import TodoForm from './components/TodoForm';
import TodoList from './components/TodoList';
import ErrorMessage from './components/ErrorMessage';
import ClearAllButton from './components/ClearAllButton';
import './App.css';

function App() {
  const { todos, loading, error, addTodo, deleteTodo, deleteAllTodos, clearError } = useTodos();

  return (
    <div className="app">
      <header className="app-header">
        <h1>Todo App</h1>
      </header>
      <main className="app-main">
        <ErrorMessage error={error} onDismiss={clearError} />
        <TodoForm onSubmit={addTodo} />
        <ClearAllButton onClearAll={deleteAllTodos} disabled={todos.length === 0} />
        <TodoList todos={todos} loading={loading} onDelete={deleteTodo} />
      </main>
    </div>
  );
}

export default App;
