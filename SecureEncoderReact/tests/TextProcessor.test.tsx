// tests/TextProcessor.test.tsx

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { vi } from 'vitest';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AppContextProvider } from '../src/context/AppContext';
import TextProcessor from '../src/components/TextProcessor';
import OperationSelector from '../src/components/OperationSelector';

type WrapperProps = {
    children: React.ReactNode;
}

// Set up mocking for the useMutation function
const mockMutate = vi.fn(() => Promise.resolve({ message: "Success" }));

vi.mock('@tanstack/react-query', async (importOriginal) => {
    const actual = await importOriginal<typeof import('@tanstack/react-query')>();
    return {
        ...actual,
        useMutation: vi.fn(() => ({
            mutate: mockMutate,
            isLoading: false,
        })),
    };
});

const queryClient = new QueryClient();

const Wrapper: React.FC<WrapperProps> = ({ children }) => (
    <QueryClientProvider client={queryClient}>
        <AppContextProvider>
            {children}
        </AppContextProvider>
    </QueryClientProvider>
);

const TestComponent = () => {
    const chooseButtonRef = React.useRef<HTMLSelectElement>(null);
    const encodingButtonRef = React.useRef<HTMLButtonElement>(null);
    const decodingButtonRef = React.useRef<HTMLButtonElement>(null);
    return (
        <div>
            <OperationSelector chooseButtonRef={chooseButtonRef} />
            <TextProcessor encodingButtonRef={encodingButtonRef} decodingButtonRef={decodingButtonRef} />
        </div>
    );
};

describe('TextProcessor Component', () => {
    beforeEach(() => {
        vi.clearAllMocks();
	});

    it('renders correctly', () => {
        render(
            <Wrapper>
                <TestComponent />
            </Wrapper>
        );
        expect(screen.getByPlaceholderText('Enter text here')).toBeInTheDocument();
    });

    it('calls processTextMutation on encode click with correct parameters', async () => {
        render(
            <Wrapper>
                <TestComponent />
            </Wrapper>
        );

        fireEvent.change(screen.getByLabelText('Select an operation'), { target: { value: 'base64' } });
        fireEvent.change(screen.getByPlaceholderText('Enter text here'), { target: { value: 'Hello, world!' } });

        const encodeButton = screen.getByText('Encode / Encrypt');
        fireEvent.click(encodeButton);

        await waitFor(() => {
			expect(screen.getByText('Encoding...')).toBeInTheDocument();
            expect(mockMutate).toHaveBeenCalled();
        });
    });

    it('shows a message when text is missing and encode is clicked', async () => {
        render(
            <Wrapper>
                <TestComponent />
            </Wrapper>
        );

        fireEvent.change(screen.getByLabelText('Select an operation'), { target: { value: 'base64' } });
		fireEvent.change(screen.getByPlaceholderText('Enter text here'), { target: { value: '' } });

        const encodeButton = screen.getByText('Encode / Encrypt');
        fireEvent.click(encodeButton);

        await waitFor(() => {
            expect(screen.getByText('Please enter text to process.')).toBeInTheDocument();
        });
    });
});
