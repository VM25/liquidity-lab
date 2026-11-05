/// <reference types="vitest/config" />
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// Flat pages with relative asset paths: the build works from any static host or sub-path (hosting is undecided).
export default defineConfig(({ isSsrBuild }) => ({
  base: './',
  plugins: [react()],
  build: isSsrBuild
    ? { outDir: '.ssr', emptyOutDir: true }
    : {
        outDir: 'dist',
        emptyOutDir: true,
        rollupOptions: {
          input: { index: 'index.html', research: 'research.html', lab: 'lab.html', methods: 'methods.html', paper: 'paper.html' },
        },
      },
  test: { environment: 'jsdom', include: ['src/**/*.test.{ts,tsx}', 'scripts/**/*.test.ts'] },
}));
