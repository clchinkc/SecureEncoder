// tests/Header.test.tsx

import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import Header from '../src/components/Header';

// Mock images
vi.mock('../src/assets/android-chrome-192x192.png', () => ({
  default: 'small_logo_mock'
}));

vi.mock('../src/assets/android-chrome-512x512.png', () => ({
  default: 'big_logo_mock'
}));

// Mock ToggleButton to render a simple button for testing
vi.mock('../src/components/ToggleButton', () => ({
  default: () => <button>Toggle</button>,
}));

describe('Header', () => {
  it('renders the title', () => {
    render(<Header title="Test Title">Test Children</Header>);
    const titleElement = screen.getByTestId('app-title');
    expect(titleElement).toBeInTheDocument();
    expect(titleElement).toHaveTextContent('Test Title');
  });

  it('renders the logo images', () => {
    render(<Header title="Test Title">Test Children</Header>);
    const logoElement = screen.getByAltText('Secure Encoder Website Logo');
    expect(logoElement).toBeInTheDocument();
    expect(logoElement).toHaveAttribute('src', 'big_logo_mock');
    expect(logoElement).toHaveStyle('backgroundImage: url(small_logo_mock)');
  });

  it('renders children when details are expanded', () => {
    render(<Header title="Test Title"><div data-testid="child-element">Test Child</div></Header>);
    const summaryElement = screen.getByText('Test Title').closest('summary');
    if (summaryElement) {
      fireEvent.click(summaryElement);
      const childElement = screen.getByTestId('child-element');
      expect(childElement).toBeInTheDocument();
      expect(childElement).toHaveTextContent('Test Child');
    } else {
      throw new Error('Summary element not found');
    }
  });

  it('renders ToggleButton component', () => {
    render(<Header title="Test Title">Test Children</Header>);
    const toggleButtonElement = screen.getByText('Toggle');
    expect(toggleButtonElement).toBeInTheDocument();
  });
});
