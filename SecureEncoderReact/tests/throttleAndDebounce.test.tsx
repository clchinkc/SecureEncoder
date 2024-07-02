// tests/throttleAndDebounce.test.tsx

import { describe, it, expect, vi } from 'vitest';
import { throttle, debounce } from '../src/utils/throttleAndDebounce';

vi.useFakeTimers();

describe('throttle', () => {
    it('should call the function immediately if enough time has passed', () => {
        const mockFn = vi.fn();
        const throttledFn = throttle(mockFn, 1000);

        throttledFn();
        expect(mockFn).toHaveBeenCalledTimes(1);
    });

    it('should not call the function again before the delay period has passed', () => {
        const mockFn = vi.fn();
        const throttledFn = throttle(mockFn, 1000);

        throttledFn();
        throttledFn();
        expect(mockFn).toHaveBeenCalledTimes(1);

        vi.advanceTimersByTime(1000);
        throttledFn();
        expect(mockFn).toHaveBeenCalledTimes(2);
    });

    it('should call the function again after the delay period has passed', () => {
        const mockFn = vi.fn();
        const throttledFn = throttle(mockFn, 1000);

        throttledFn();
        vi.advanceTimersByTime(500);
        throttledFn();
        expect(mockFn).toHaveBeenCalledTimes(1);

        vi.advanceTimersByTime(500);
        throttledFn();
        expect(mockFn).toHaveBeenCalledTimes(2);
    });
});

describe('debounce', () => {
    it('should call the function after the delay period has passed', () => {
        const mockFn = vi.fn();
        const debouncedFn = debounce(mockFn, 1000);

        debouncedFn();
        expect(mockFn).not.toHaveBeenCalled();

        vi.advanceTimersByTime(1000);
        expect(mockFn).toHaveBeenCalledTimes(1);
    });

    it('should reset the delay period if called again before the delay period has passed', () => {
        const mockFn = vi.fn();
        const debouncedFn = debounce(mockFn, 1000);

        debouncedFn();
        vi.advanceTimersByTime(500);
        debouncedFn();
        vi.advanceTimersByTime(500);
        expect(mockFn).not.toHaveBeenCalled();

        vi.advanceTimersByTime(500);
        expect(mockFn).toHaveBeenCalledTimes(1);
    });

    it('should call the function once if called multiple times within the delay period', () => {
        const mockFn = vi.fn();
        const debouncedFn = debounce(mockFn, 1000);

        debouncedFn();
        debouncedFn();
        debouncedFn();
        vi.advanceTimersByTime(1000);
        expect(mockFn).toHaveBeenCalledTimes(1);
    });
});
