import { defineConfig } from '@playwright/test';

// Uses the locally installed Google Chrome (no browser download); serves the production build with `next start`.
export default defineConfig({
  testDir: 'e2e',
  timeout: 30_000,
  reporter: [['list']],
  use: { baseURL: 'http://localhost:4324', channel: 'chrome', headless: true },
  webServer: { command: 'npx next start --port 4324', url: 'http://localhost:4324/', reuseExistingServer: false, timeout: 60_000 },
});
