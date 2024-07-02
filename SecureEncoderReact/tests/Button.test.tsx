// tests/Button.test.tsx

import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import Button from '../src/components/Button';

describe('Button', () => {
  it('renders children correctly', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('applies base styles', () => {
    render(<Button>Base Button</Button>);
    const button = screen.getByRole('button');
    expect(button).toHaveClass('py-2 px-2 rounded-lg inline-block text-center transition-colors duration-200 ease-in-out');
  });

  it('applies primary button styles', () => {
    render(<Button type="button-primary">Primary Button</Button>);
    const button = screen.getByRole('button');
    expect(button).toHaveClass('bg-blue-700 text-neutral-100 hover:bg-blue-900 dark:bg-blue-500 dark:hover:bg-blue-700');
  });

  it('applies secondary button styles', () => {
    render(<Button type="button-secondary">Secondary Button</Button>);
    const button = screen.getByRole('button');
    expect(button).toHaveClass('bg-neutral-700 text-neutral-100 hover:bg-neutral-900 dark:bg-neutral-500 dark:hover:bg-neutral-700');
  });

  it('applies outline styles for primary button', () => {
    render(<Button type="button-primary" outline>Outline Primary</Button>);
    const button = screen.getByRole('button');
    expect(button).toHaveClass('border border-blue-700 text-blue-700 hover:bg-blue-700 hover:text-neutral-100 dark:border-blue-300 dark:text-blue-300 dark:hover:bg-blue-300 dark:hover:text-black');
  });

  it('applies outline styles for secondary button', () => {
    render(<Button type="button-secondary" outline>Outline Secondary</Button>);
    const button = screen.getByRole('button');
    expect(button).toHaveClass('border border-neutral-700 text-neutral-700 hover:bg-neutral-700 hover:text-neutral-100 dark:border-neutral-300 dark:text-neutral-300 dark:hover:bg-neutral-300 dark:hover:text-black');
  });

  it('applies custom className', () => {
    render(<Button className="custom-class">Custom Class Button</Button>);
    const button = screen.getByRole('button');
    expect(button).toHaveClass('custom-class');
  });

  it('applies disabled styles', () => {
    render(<Button disabled>Disabled Button</Button>);
    const button = screen.getByRole('button');
    expect(button).toHaveClass('cursor-not-allowed opacity-50');
  });

  it('calls onClick when clicked and not disabled', () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Clickable Button</Button>);
    const button = screen.getByRole('button');
    fireEvent.click(button);
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('does not call onClick when clicked and disabled', () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick} disabled>Disabled Button</Button>);
    const button = screen.getByRole('button');
    fireEvent.click(button);
    expect(handleClick).not.toHaveBeenCalled();
  });

  it('calls showAlert when clicked and disabled', () => {
    const showAlert = vi.fn();
    render(<Button disabled showAlert={showAlert}>Alert Button</Button>);
    const button = screen.getByRole('button');
    fireEvent.click(button);
    expect(showAlert).toHaveBeenCalledTimes(1);
  });

  it('forwards ref correctly', () => {
    const ref = vi.fn();
    render(<Button ref={ref}>Ref Button</Button>);
    expect(ref).toHaveBeenCalledWith(expect.any(HTMLButtonElement));
  });
});