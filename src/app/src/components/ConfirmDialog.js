import React from 'react';

function ConfirmDialog({ isOpen, message, onConfirm, onCancel }) {
  if (!isOpen) return null;

  return (
    <div className="confirm-overlay">
      <div className="confirm-dialog">
        <p className="confirm-message">{message}</p>
        <div className="confirm-buttons">
          <button className="confirm-btn confirm-yes" onClick={onConfirm}>Yes</button>
          <button className="confirm-btn confirm-no" onClick={onCancel}>No</button>
        </div>
      </div>
    </div>
  );
}

export default ConfirmDialog;
