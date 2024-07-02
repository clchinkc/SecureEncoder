// tests/Home.test.tsx

import { describe, it, expect, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import type { ReactNode } from 'react';
import Home from '../src/pages/Home';

// Mock any other necessary components or contexts
vi.mock('../context/AppContext', () => ({
  AppContextProvider: ({ children }: { children: ReactNode }) => <div>{children}</div>
}));

vi.mock('../components/ErrorBoundary', () => ({ children }: { children: ReactNode }) => <>{children}</>);

const queryClient = new QueryClient();

describe('Home Component', () => {
  it('renders correctly', async () => {
    const mockRef = () => ({
      current: null
    });
    const props = {
      uploadButtonRef: mockRef(),
      fileSelectionRef: mockRef(),
      chooseButtonRef: mockRef(),
      encodingButtonRef: mockRef(),
      decodingButtonRef: mockRef(),
      copyToClipboardRef: mockRef(),
      downloadFileRef: mockRef(),
    };

    render(
      <QueryClientProvider client={queryClient}>
        <Home {...props} />
      </QueryClientProvider>
    );

    await waitFor(() => {
      expect(screen.getByText('Secure Encoder')).toBeInTheDocument();
      expect(screen.getByText(/Encode and decode text using various algorithms and keys./)).toBeInTheDocument();
    });
  });

  // Additional tests can be added here
});
