/// <reference types="vitest" />
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'
import tsconfigPaths from 'vite-tsconfig-paths'

// https://vitejs.dev/config https://vitest.dev/config
export default defineConfig({
  plugins: [react(), tsconfigPaths()],
  test: {
    globals: true,
    environment: 'happy-dom',
    setupFiles: '.vitest/setup',
    include: ['tests/*.{test,spec}.{js,jsx,ts,tsx}'],
    exclude: [
      '**/node_modules/**',
      '**/dist/**',
      '**/cypress/**',
      '**/.{idea,git,cache,output,temp}/**',
      '**/{karma,rollup,webpack,vite,vitest,jest,ava,babel,nyc,cypress,tsup,build,production,eslint,prettier}.config.*'
    ]
  },
  preview: {
    strictPort: true,
    port: 3000,
   },
  server: {
    open: true,
    host: true,
    strictPort: true,
    port: 3000,
  },
  build: {
    outDir: 'build',
    minify: 'esbuild',
    sourcemap: true,
    target: 'esnext',
  }
})
