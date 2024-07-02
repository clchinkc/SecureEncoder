import postcssConfig from '/postcss.config.mjs';

test('postcss config loads correctly', () => {
    expect(postcssConfig).toBeDefined();
});
