// tests/ResultDisplay.test.tsx

import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { render, screen, act } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { AppContextProvider } from '../src/context/AppContext';
import ResultDisplay from '../src/components/ResultDisplay';

describe('ResultDisplay Component', () => {
    beforeEach(() => {
      // Define a writable property for the clipboard
      const clipboardMock = {
        writeText: vi.fn(),
      };
      Object.defineProperty(globalThis.navigator, 'clipboard', {
        value: clipboardMock,
        writable: true,
        configurable: true
      });
    });
  
    afterEach(() => {
      // Cleanup and restore any mocks after each test
      vi.restoreAllMocks();
    });
  
    const setup = (result: string | null = null, operation: string = '') => {
      // Handle null values appropriately
      const sanitizedResult = result ?? undefined;
      return render(
        <AppContextProvider value={{ result: sanitizedResult, operation }}>
          <ResultDisplay
            copyToClipboardRef={{ current: document.createElement('button') }}
            downloadFileRef={{ current: document.createElement('button') }}
          />
        </AppContextProvider>
      );
    };
  
    it('copy to clipboard success', async () => {
        navigator.clipboard.writeText = vi.fn().mockResolvedValue(undefined);
        setup("Test result", "Test Operation");

        await act(async () => {
            userEvent.click(screen.getByText(/Copy to Clipboard/i));
        });

        await screen.findByText("Copied to clipboard!");
        expect(navigator.clipboard.writeText).toHaveBeenCalledWith("Test result");
    });
  
    it('copy to clipboard failure', async () => {
        const errorMessage = "Failed to copy";
        navigator.clipboard.writeText = vi.fn().mockRejectedValue(new Error(errorMessage));
        setup("Test result", "Test Operation");

        await act(async () => {
            userEvent.click(screen.getByText(/Copy to Clipboard/i));
        });

        await screen.findByText(new RegExp(errorMessage, 'i'));
        expect(navigator.clipboard.writeText).toHaveBeenCalledWith("Test result");
    });
  });
