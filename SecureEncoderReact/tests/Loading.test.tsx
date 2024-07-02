// tests/Loading.test.tsx

import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import Loading from '../src/components/Loading';

describe('Loading', () => {
  it('renders the skeleton loader', () => {
    render(<Loading />);
    const skeletonLoader = screen.getByTestId('skeleton-loader');
    expect(skeletonLoader).toBeInTheDocument();
  });

  it('renders the correct number of skeleton elements', () => {
    render(<Loading />);
    const skeletonElements = screen.getAllByTestId('skeleton-element');
    expect(skeletonElements).toHaveLength(3);
  });

  it('renders skeleton elements with correct classes', () => {
    render(<Loading />);
    const skeletonElements = screen.getAllByTestId('skeleton-element');
    skeletonElements.forEach(element => {
      expect(element).toHaveClass('mb-2 h-4 rounded bg-gray-300');
    });
  });
});
