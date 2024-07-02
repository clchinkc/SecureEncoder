// tests/index.test.tsx

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { QueryClient } from '@tanstack/react-query';
import ReactDOM, { Root } from 'react-dom/client';


describe('Index', () => {
  let root: HTMLElement;
  let queryClient: QueryClient;

  beforeEach(() => {
    queryClient = new QueryClient();
    root = document.createElement('div');
    root.id = 'root';
    document.body.appendChild(root);

    // Mock ReactDOM.createRoot
    vi.spyOn(ReactDOM, 'createRoot').mockImplementation(() => {
      return {
        render: vi.fn(),
        unmount: vi.fn(),
      } as unknown as Root;
    });
  });

  afterEach(() => {
    document.body.removeChild(root);
    vi.restoreAllMocks();
  });

  it('renders without crashing', async () => {
    // Import index.tsx here to execute it
    await import('../src/index');

    // Verify that the mocked render function was called
    expect(ReactDOM.createRoot).toHaveBeenCalledWith(root);
  });
});
