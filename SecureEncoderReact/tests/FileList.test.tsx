// tests/FileList.test.tsx

import { describe, it, expect, vi, beforeAll, afterAll, afterEach } from 'vitest';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { QueryClient, QueryClientProvider, useQuery } from '@tanstack/react-query';
import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';
import FileList from '../src/components/FileList';

// Setup environment variable
import.meta.env.VITE_APP_FLASK_URL = 'http://localhost:5000';

// Mock react-query
vi.mock('@tanstack/react-query', async (importOriginal) => {
  const mod = await importOriginal<typeof import('@tanstack/react-query')>();
  return {
    ...mod,
    useQuery: vi.fn(),
  };
});

// Setup MSW server
const server = setupServer(
  http.get('http://localhost:5000/api/files', () => {
    return HttpResponse.json(['file1.pem', 'file2.pem']);
  }),
  http.get('http://localhost:5000/api/download_key/:filename', () => {
    return new HttpResponse(new Blob(['file content']), {
      headers: { 'Content-Type': 'application/octet-stream' },
    });
  }),
  http.delete('http://localhost:5000/api/delete_key/:filename', () => {
    return HttpResponse.json({ message: 'File deleted successfully' });
  })
);

beforeAll(() => server.listen());
afterAll(() => server.close());
afterEach(() => {
  server.resetHandlers();
  vi.restoreAllMocks();
});

// Setup QueryClient
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
    },
  },
});

const renderWithQueryClient = (component: React.ReactElement) => {
  return render(
    <QueryClientProvider client={queryClient}>
      {component}
    </QueryClientProvider>
  );
};

describe('FileList', () => {
  it('renders loading state with "Loading..." text', async () => {
    vi.mocked(useQuery).mockReturnValue({
      isLoading: true,
      error: null,
      data: undefined,
    } as any);

    renderWithQueryClient(<FileList />);

    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  it('renders placeholder files in table during loading state', async () => {
    vi.mocked(useQuery).mockReturnValue({
      isLoading: false,
      error: null,
      data: Array(3)
        .fill('')
        .map((_, idx) => `loading-file-${idx}.pem`),
    } as any);

    renderWithQueryClient(<FileList />);

    await waitFor(() => {
      const rows = screen.getAllByRole('row');
      expect(rows[1]).toHaveTextContent('loading-file-0.pem');
      expect(rows[2]).toHaveTextContent('loading-file-1.pem');
      expect(rows[3]).toHaveTextContent('loading-file-2.pem');
    });
  });

  it('renders file list after loading', async () => {
    vi.mocked(useQuery).mockReturnValue({
      isLoading: false,
      error: null,
      data: ['file1.pem', 'file2.pem'],
    } as any);

    renderWithQueryClient(<FileList />);
    await waitFor(() => {
      expect(screen.getByText('file1.pem')).toBeInTheDocument();
      expect(screen.getByText('file2.pem')).toBeInTheDocument();
    });
  });

  it('handles error when fetching files', async () => {
    vi.mocked(useQuery).mockReturnValue({
      isLoading: false,
      error: new Error('Failed to load files'),
      data: undefined,
    } as any);

    renderWithQueryClient(<FileList />);

    await waitFor(() => {
      expect(screen.getByText('Error: Failed to load files')).toBeInTheDocument();
    });
  });

  it('handles download button click', async () => {
    vi.mocked(useQuery).mockReturnValue({
      isLoading: false,
      error: null,
      data: ['file1.pem'],
    } as any);

    renderWithQueryClient(<FileList />);
    
    const downloadButton = await screen.findByText('Download');
    fireEvent.click(downloadButton);

    await waitFor(() => {
      expect(screen.getByText('File downloaded successfully!')).toBeInTheDocument();
    });
  });

  it('handles delete button click', async () => {
    vi.mocked(useQuery).mockReturnValue({
      isLoading: false,
      error: null,
      data: ['file1.pem'],
    } as any);

    renderWithQueryClient(<FileList />);
    
    const deleteButton = await screen.findByText('Delete');
    fireEvent.click(deleteButton);

    await waitFor(() => {
      expect(screen.getByText('File deleted successfully')).toBeInTheDocument();
    });
  });
});
