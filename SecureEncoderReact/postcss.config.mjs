import tailwindcss from 'tailwindcss'
import autoprefixer from 'autoprefixer'
import purgecss from '@fullhuman/postcss-purgecss'

export default {
  plugins: [
    tailwindcss,
    autoprefixer,
    purgecss({
      content: ['./src/**/*.{js,jsx,ts,tsx}', './index.html'],
      safelist: ['html', 'body'],
      defaultExtractor: (content) => content.match(/[\w-/:]+(?<!:)/g) || [],
      css: ['./src/assets/*.css'],
      output: './build'
    })
  ]
};
