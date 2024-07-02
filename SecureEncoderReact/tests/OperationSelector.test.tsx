// tests/OperationSelector.test.tsx

import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';
import OperationSelector from '../src/components/OperationSelector';
import { AppContextProvider } from '../src/context/AppContext';

describe('OperationSelector', () => {
    // Mocks ref for testing
    const mockRef = React.createRef<HTMLSelectElement>();
  
    // Test for basic rendering
    it('renders without crashing', () => {
      render(
        <AppContextProvider>
          <OperationSelector chooseButtonRef={mockRef} />
        </AppContextProvider>
      );
      expect(screen.getByLabelText('Select an operation')).toBeInTheDocument();
    });
  
    // Test select interaction
    it('allows selection of operation', () => {
      render(
        <AppContextProvider>
          <OperationSelector chooseButtonRef={mockRef} />
        </AppContextProvider>
      );
      const selectElement = screen.getByLabelText('Select an operation') as HTMLSelectElement;
      fireEvent.change(selectElement, { target: { value: 'base64' } });
      expect(selectElement.value).toBe('base64');
    });
  
    // Test if the ref is being used correctly
    it('uses the provided ref correctly', () => {
      render(
        <AppContextProvider>
          <OperationSelector chooseButtonRef={mockRef} />
        </AppContextProvider>
      );
      expect(mockRef.current).toBeTruthy();
    });
  
    // Test for accessibility concerns
    it('should have proper aria attributes for accessibility', () => {
      render(
        <AppContextProvider>
          <OperationSelector chooseButtonRef={mockRef} />
        </AppContextProvider>
      );
      const selectElement = screen.getByLabelText('Select an operation') as HTMLSelectElement;
      expect(selectElement.getAttribute('aria-live')).toBe('polite');
    });
  });