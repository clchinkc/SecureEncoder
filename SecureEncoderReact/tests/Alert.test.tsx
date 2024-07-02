// tests/Alert.test.tsx

import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import Alert from '../src/components/Alert';

describe('Alert', () => {
  it('renders children correctly', () => {
    render(<Alert type="alert-info">Test message</Alert>);
    expect(screen.getByText('Test message')).toBeInTheDocument();
  });

  it('applies correct base styles', () => {
    render(<Alert type="alert-info">Test message</Alert>);
    const alert = screen.getByRole('alert');
    expect(alert).toHaveClass('rounded-lg px-2 py-2');
  });

  it('applies correct styles for alert-info type', () => {
    render(<Alert type="alert-info">Info alert</Alert>);
    const alert = screen.getByRole('alert');
    expect(alert).toHaveClass('bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100');
  });

  it('applies correct styles for alert-success type', () => {
    render(<Alert type="alert-success">Success alert</Alert>);
    const alert = screen.getByRole('alert');
    expect(alert).toHaveClass('bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100');
  });

  it('applies correct styles for alert-danger type', () => {
    render(<Alert type="alert-danger">Danger alert</Alert>);
    const alert = screen.getByRole('alert');
    expect(alert).toHaveClass('bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100');
  });

  it('applies default styles when type is null', () => {
    render(<Alert type={null}>Default alert</Alert>);
    const alert = screen.getByRole('alert');
    expect(alert).toHaveClass('bg-neutral-100 text-neutral-800 dark:bg-neutral-900 dark:text-neutral-100');
  });

  it('has correct accessibility attributes', () => {
    render(<Alert type="alert-info">Accessible alert</Alert>);
    const alert = screen.getByRole('alert');
    expect(alert).toHaveAttribute('aria-live', 'assertive');
  });
});