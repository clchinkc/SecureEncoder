// tests/ToggleButton.test.tsx

import { fireEvent, render, screen } from '@testing-library/react';
import ToggleButton from '../src/components/ToggleButton';

describe('ToggleButton', () => {
  beforeEach(() => {
    // Clear all items in localStorage
    localStorage.clear();
  });

  it('should initialize in light mode if local storage has no entry', () => {
    render(<ToggleButton />);
    const checkbox = screen.getByRole('checkbox');
    expect(checkbox).not.toBeChecked();
    expect(document.documentElement.classList.contains('dark')).toBe(false);
  });

  it('should initialize in dark mode if local storage indicates dark mode', () => {
    localStorage.setItem('dark-mode', 'true');
    render(<ToggleButton />);
    const checkbox = screen.getByRole('checkbox');
    expect(checkbox).toBeChecked();
    expect(document.documentElement.classList.contains('dark')).toBe(true);
  });

  it('toggles dark mode on click', () => {
    render(<ToggleButton />);
    const checkbox = screen.getByRole('checkbox');

    // Toggle on
    fireEvent.click(checkbox);
    expect(checkbox).toBeChecked();
    expect(document.documentElement.classList.contains('dark')).toBe(true);
    expect(localStorage.getItem('dark-mode')).toBe('true');

    // Toggle off
    fireEvent.click(checkbox);
    expect(checkbox).not.toBeChecked();
    expect(document.documentElement.classList.contains('dark')).toBe(false);
    expect(localStorage.getItem('dark-mode')).toBe('false');
  });

  it('should correctly toggle the dark class on the document root', () => {
    render(<ToggleButton />);
    const checkbox = screen.getByRole('checkbox');

    // First click - Enable Dark Mode
    fireEvent.click(checkbox);
    expect(document.documentElement.classList).toContain('dark');

    // Second click - Disable Dark Mode
    fireEvent.click(checkbox);
    expect(document.documentElement.classList).not.toContain('dark');
  });
});
