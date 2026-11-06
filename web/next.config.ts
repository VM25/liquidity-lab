import type { NextConfig } from 'next';

// Every page is prerendered at build time (static rendering); there are no API routes, server actions or middleware.
const nextConfig: NextConfig = {
  reactStrictMode: true,
  poweredByHeader: false,
  // The pre-Next.js build served flat files (lab.html#step=3); keep those addresses working.
  async redirects() {
    return [
      { source: '/index.html', destination: '/', permanent: true },
      ...['lab', 'research', 'methods', 'paper'].map((p) => ({ source: `/${p}.html`, destination: `/${p}`, permanent: true })),
    ];
  },
};

export default nextConfig;
