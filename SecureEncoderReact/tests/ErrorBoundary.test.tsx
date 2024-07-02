// tests/ErrorBoundary.test.tsx

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, act, waitFor } from '@testing-library/react';
import ErrorBoundary from '../src/components/ErrorBoundary';

// Create a component that throws an error
const ErrorComponent = () => {
  throw new Error('Test error');
};

// Create a component that doesn't throw an error
const NormalComponent = () => <div>Normal component</div>;

describe('ErrorBoundary', () => {
  beforeEach(() => {
    vi.spyOn(console, 'error').mockImplementation(() => {});
  });

  it('renders children when there is no error', () => {
    render(
      <ErrorBoundary>
        <NormalComponent />
      </ErrorBoundary>
    );

    expect(screen.getByText('Normal component')).toBeInTheDocument();
  });

  it('renders error message when child component throws', () => {
    render(
      <ErrorBoundary>
        <ErrorComponent />
      </ErrorBoundary>
    );

    expect(screen.getByText('Something unexpected happened. Please try again later.')).toBeInTheDocument();
  });

  it('calls console.error when an error is caught', () => {
    render(
      <ErrorBoundary>
        <ErrorComponent />
      </ErrorBoundary>
    );

    expect(console.error).toHaveBeenCalled();
  });

  it('resets error state when new children are received', async () => {
    const { rerender } = render(
      <ErrorBoundary>
        <ErrorComponent />
      </ErrorBoundary>
    );

    expect(screen.getByText('Something unexpected happened. Please try again later.')).toBeInTheDocument();

    await act(async () => {
      rerender(
        <ErrorBoundary>
          <NormalComponent />
        </ErrorBoundary>
      );
    });

    await waitFor(() => {
      expect(screen.getByText('Normal component')).toBeInTheDocument();
    });
  });
});
