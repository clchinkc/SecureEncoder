// tests/KeyUploader.test.tsx

import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import KeyUploader from '../src/components/KeyUploader';

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

describe('KeyUploader', () => {
  const mockUploadButtonRef = { current: null };
  const mockFileSelectionRef = { current: null };

  beforeEach(() => {
    vi.resetAllMocks();
  });

  it('renders the component', () => {
    renderWithQueryClient(<KeyUploader uploadButtonRef={mockUploadButtonRef} fileSelectionRef={mockFileSelectionRef} />);
    expect(screen.getByText('Upload Existing Key:')).toBeInTheDocument();
  });

  it('shows an alert when no file is selected and upload is clicked', () => {
    renderWithQueryClient(<KeyUploader uploadButtonRef={mockUploadButtonRef} fileSelectionRef={mockFileSelectionRef} />);
    
    const uploadButton = screen.getByText('Upload');
    fireEvent.click(uploadButton);
    
    expect(screen.getByText('Please select a file to upload.')).toBeInTheDocument();
  });

  it('handles file selection', () => {
    renderWithQueryClient(<KeyUploader uploadButtonRef={mockUploadButtonRef} fileSelectionRef={mockFileSelectionRef} />);
    
    const fileInput = screen.getByLabelText('file');
    const file = new File(['(⌐□_□)'], 'test.pem', { type: 'application/x-pem-file' });
    
    fireEvent.change(fileInput, { target: { files: [file] } });
    
    expect(screen.queryByText('Please select a file to upload.')).not.toBeInTheDocument();
  });

  it('uploads a selected file successfully', async () => {
    // Mock fetch response
    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({}),
      })
    ) as unknown as typeof fetch;

    renderWithQueryClient(<KeyUploader uploadButtonRef={mockUploadButtonRef} fileSelectionRef={mockFileSelectionRef} />);
    
    const fileInput = screen.getByLabelText('file');
    const file = new File(['(⌐□_□)'], 'test.pem', { type: 'application/x-pem-file' });
    
    fireEvent.change(fileInput, { target: { files: [file] } });
    
    const uploadButton = screen.getByText('Upload');
    fireEvent.click(uploadButton);

    await waitFor(() => {
      expect(screen.getByText('File test.pem uploaded successfully!')).toBeInTheDocument();
    });
  });

  it('handles file upload error', async () => {
    // Mock fetch response
    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: false,
        json: () => Promise.resolve({ message: 'Upload failed' }),
      })
    ) as unknown as typeof fetch;

    renderWithQueryClient(<KeyUploader uploadButtonRef={mockUploadButtonRef} fileSelectionRef={mockFileSelectionRef} />);
    
    const fileInput = screen.getByLabelText('file');
    const file = new File(['(⌐□_□)'], 'test.pem', { type: 'application/x-pem-file' });
    
    fireEvent.change(fileInput, { target: { files: [file] } });
    
    const uploadButton = screen.getByText('Upload');
    fireEvent.click(uploadButton);

    await waitFor(() => {
      expect(screen.getByText('Error: Upload failed')).toBeInTheDocument();
    });
  });
});

