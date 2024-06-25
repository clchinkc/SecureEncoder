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
    include: ['**/test.{ts,tsx}']
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
