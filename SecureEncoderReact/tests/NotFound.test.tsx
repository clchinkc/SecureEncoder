// tests/NotFound.test.tsx

import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import NotFound from '../src/pages/NotFound';

describe('NotFound Component', () => {
  it('renders correctly', () => {
    render(<NotFound />);
    const headingElement = screen.getByRole('heading', { name: /404 not found/i });
    const paragraphElement = screen.getByText(/the page you are looking for does not exist\./i);

    expect(headingElement).toBeInTheDocument();
    expect(paragraphElement).toBeInTheDocument();
  });
});
