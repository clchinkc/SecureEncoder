// tests/App.test.tsx

import { describe, it, expect, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import App from '../src/App';



describe('App', () => {
  let queryClient: QueryClient;

  beforeEach(() => {
    queryClient = new QueryClient();
  });

  it('renders the Home page for the root route', async () => {
    render(
      <QueryClientProvider client={queryClient}>
        <MemoryRouter initialEntries={['/']}>
          <App />
        </MemoryRouter>
      </QueryClientProvider>
    );

    const titleElement = await screen.findByTestId('app-title');
    expect(titleElement).toBeInTheDocument();
    expect(titleElement.textContent).toBe('Secure Encoder');
  });

  it('renders the NotFound page for an unknown route', () => {
    render(
      <QueryClientProvider client={queryClient}>
        <MemoryRouter initialEntries={['/unknown-route']}>
          <App />
        </MemoryRouter>
      </QueryClientProvider>
    );

    // Assuming your NotFound component has a "404" text or similar
    expect(screen.getByText(/404 Not Found/i)).toBeInTheDocument();
  });

  it('applies dynamic font sizing based on window size', () => {
    const { container } = render(
      <QueryClientProvider client={queryClient}>
        <MemoryRouter>
          <App />
        </MemoryRouter>
      </QueryClientProvider>
    );

    // Trigger a resize event
    window.dispatchEvent(new Event('resize'));

    // Check if the font size has been set on the document element
    const htmlElement = container.ownerDocument.documentElement;
    expect(htmlElement.style.fontSize).not.toBe('');
  });
});