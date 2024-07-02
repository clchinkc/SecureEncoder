// tests/Card.test.tsx

import { describe, it, expect } from 'vitest';
import { render, screen, act } from '@testing-library/react';
import Card from '../src/components/Card';

// Helper function to create a component that suspends
const createSuspendedComponent = () => {
    let status = 'pending';
    let result: any;
    let suspender = new Promise<void>((resolve) => {
      setTimeout(() => {
        status = 'success';
        result = 'Async content';
        resolve();
      }, 100);
    });
  
    return {
      SuspendedComponent: () => {
        if (status === 'pending') {
          throw suspender;
        }
        return <div>{result}</div>;
      }
    };
  };
  
  describe('Card', () => {
    it('renders children correctly', () => {
      render(
        <Card>
          <div>Card content</div>
        </Card>
      );
      expect(screen.getByText('Card content')).toBeInTheDocument();
    });
  
    it('applies correct base styles', () => {
      render(<Card><div>Test</div></Card>);
      const card = screen.getByText('Test').closest('.card');
      expect(card).toHaveClass('mb-3 flex flex-col border border-neutral-300 bg-neutral-100 p-3 dark:border-neutral-700 dark:bg-neutral-900');
    });
  
    it('uses Loading component as default fallback', async () => {
      const { SuspendedComponent } = createSuspendedComponent();
      await act(async () => {
        render(
          <Card>
            <SuspendedComponent />
          </Card>
        );
      });
      expect(screen.getByTestId('skeleton-loader')).toBeInTheDocument();
    });
  
    it('uses custom fallback when provided', async () => {
      const { SuspendedComponent } = createSuspendedComponent();
      const customFallback = <div data-testid="custom-fallback">Custom loading...</div>;
      await act(async () => {
        render(
          <Card fallback={customFallback}>
            <SuspendedComponent />
          </Card>
        );
      });
      expect(screen.getByTestId('custom-fallback')).toBeInTheDocument();
    });
  
    it('wraps children in Suspense', async () => {
      const { SuspendedComponent } = createSuspendedComponent();
      await act(async () => {
        render(
          <Card>
            <SuspendedComponent />
          </Card>
        );
      });
      expect(screen.getByTestId('skeleton-loader')).toBeInTheDocument();
      
      // Wait for the suspended component to resolve
      await act(async () => {
        await new Promise(resolve => setTimeout(resolve, 150));
      });
      
      expect(screen.getByText('Async content')).toBeInTheDocument();
    });
  });