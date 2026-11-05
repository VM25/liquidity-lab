import { defineConfig } from '@playwright/test';

// Uses the locally installed Google Chrome (no browser download); serves the built site with `vite preview`.
export default defineConfig({
  testDir: 'e2e',
  timeout: 30_000,
  reporter: [['list']],
  use: { baseURL: 'http://localhost:4324/', channel: 'chrome', headless: true },
  webServer: { command: 'npx vite preview --port 4324 --strictPort', url: 'http://localhost:4324/index.html', reuseExistingServer: false, timeout: 60_000 },
});
