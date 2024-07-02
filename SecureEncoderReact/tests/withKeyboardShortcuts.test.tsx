// tests/withKeyboardShortcuts.test.tsx

import { fireEvent, render } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import withKeyboardShortcuts from '../src/hoc/withKeyboardShortcuts';

const MockComponent = () => {
    return <button>Upload</button>;
};

describe('withKeyboardShortcuts HOC', () => {
    it('passes refs to the wrapped component', () => {
      const EnhancedComponent = withKeyboardShortcuts(MockComponent, () => ({}));
      const { getByText } = render(<EnhancedComponent />);
      const button = getByText('Upload');
      expect(button.tagName).toBe('BUTTON');
    });

    it('calls functions based on key press', () => {
      const mockFunction = vi.fn();
      const keyMapFunction = vi.fn(() => ({ 'a': mockFunction }));

      const EnhancedComponent = withKeyboardShortcuts(MockComponent, keyMapFunction);
      render(<EnhancedComponent />);

      fireEvent.keyDown(window, { key: 'A', altKey: true });
      
      expect(keyMapFunction).toHaveBeenCalled();
      expect(mockFunction).toHaveBeenCalled();
    });

    it('cleans up event listeners on unmount', () => {
      const EnhancedComponent = withKeyboardShortcuts(MockComponent, () => ({ 'a': vi.fn() }));
      const { unmount } = render(<EnhancedComponent />);
      
      const removeEventListenerSpy = vi.spyOn(window, 'removeEventListener');
      unmount();
      
      expect(removeEventListenerSpy).toHaveBeenCalledWith('keydown', expect.any(Function));
    });
});
