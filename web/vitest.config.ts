import { defineConfig } from 'vitest/config';

// Unit tests only; the site itself is built by Next.js.
export default defineConfig({
  test: { environment: 'jsdom', include: ['src/**/*.test.{ts,tsx}', 'scripts/**/*.test.ts'] },
});
