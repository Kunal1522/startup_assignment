import React from 'react';

class ErrorLogger {
  static log(error, context = '') {
    const timestamp = new Date().toISOString();
    console.error(`[${timestamp}] ${context}: ${error}`);
  }
}

function ErrorMessage({ error, onDismiss }) {
  if (!error) return null;

  ErrorLogger.log(error, 'UI Error Display');

  return (
    <div className="error-message">
      <span>{error}</span>
      <button onClick={onDismiss} className="error-dismiss">&times;</button>
    </div>
  );
}

export { ErrorLogger };
export default ErrorMessage;
