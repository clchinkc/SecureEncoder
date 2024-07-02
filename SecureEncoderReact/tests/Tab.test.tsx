// src/components/Tabs.test.tsx

import { render, screen, fireEvent } from "@testing-library/react";
import { AppContextProvider, useAppContext } from "../src/context/AppContext";
import Tabs from "../src/components/Tabs";

// Mock AppContext to use in the tests
const MockedComponent = () => {
    const { operation } = useAppContext();
    return (
        <div>
            <Tabs />
            <div data-testid="current-operation">{operation}</div>
        </div>
    );
};

describe("Tabs Component", () => {
    it("renders all options", () => {
        render(
            <AppContextProvider>
                <MockedComponent />
            </AppContextProvider>
        );
        const options = [
            "Base64",
            "Hex",
            "UTF-8",
            "Latin-1",
            "ASCII",
            "URL",
            "AES",
            "RSA",
            "MD5",
            "Huffman",
            "LZ77",
            "LZW",
            "Zstd",
            "Deflate",
            "Brotli",
        ];
        options.forEach((option) => {
            expect(screen.getByText(option)).toBeInTheDocument();
        });
    });

    it("changes operation on click", () => {
        render(
            <AppContextProvider>
                <MockedComponent />
            </AppContextProvider>
        );

        const option = screen.getByText("Hex");
        fireEvent.click(option);

        const currentOperation = screen.getByTestId("current-operation");
        expect(currentOperation).toHaveTextContent("hex");
    });

    it("applies correct styles on selection", () => {
        render(
            <AppContextProvider>
                <MockedComponent />
            </AppContextProvider>
        );

        const option = screen.getByText("Hex");
        fireEvent.click(option);

        expect(option.parentElement).toHaveClass("bg-neutral-100 text-neutral-700 dark:bg-neutral-700 dark:text-neutral-100");

        const otherOption = screen.getByText("Base64");
        expect(otherOption.parentElement).toHaveClass("bg-neutral-300 text-neutral-900 dark:bg-neutral-900 dark:text-neutral-300");
    });
});
