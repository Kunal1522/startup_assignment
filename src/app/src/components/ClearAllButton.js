import React, { useState, useCallback } from 'react';
import ConfirmDialog from './ConfirmDialog';

function ClearAllButton({ onClearAll, disabled }) {
  const [showConfirm, setShowConfirm] = useState(false);

  const handleClick = useCallback(() => setShowConfirm(true), []);
  const handleCancel = useCallback(() => setShowConfirm(false), []);

  const handleConfirm = useCallback(async () => {
    setShowConfirm(false);
    await onClearAll();
  }, [onClearAll]);

  return (
    <>
      <button
        className="clear-all-btn"
        onClick={handleClick}
        disabled={disabled}
      >
        Clear All Todos
      </button>
      <ConfirmDialog
        isOpen={showConfirm}
        message="Are you sure you want to delete all todos?"
        onConfirm={handleConfirm}
        onCancel={handleCancel}
      />
    </>
  );
}

export default ClearAllButton;
