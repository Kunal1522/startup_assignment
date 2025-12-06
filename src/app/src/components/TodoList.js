import React from 'react';

function TodoItem({ todo, onDelete }) {
  return (
    <li className="todo-item">
      <div className="todo-content">
        <span className="todo-text">{todo.text}</span>
        <span className="todo-date">{new Date(todo.created_at).toLocaleDateString()}</span>
      </div>
      <button className="todo-delete-btn" onClick={() => onDelete(todo.id)} title="Delete">
        ×
      </button>
    </li>
  );
}

function TodoList({ todos, loading, onDelete }) {
  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  if (todos.length === 0) {
    return <p className="empty-message">No todos yet. Add one above!</p>;
  }

  return (
    <ul className="todo-list">
      {todos.map(todo => <TodoItem key={todo.id} todo={todo} onDelete={onDelete} />)}
    </ul>
  );
}

export default TodoList;
