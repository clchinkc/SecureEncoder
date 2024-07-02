import tailwindConfig from '/tailwind.config.mjs';

test('tailwind config loads correctly', () => {
    expect(tailwindConfig).toBeDefined();
});