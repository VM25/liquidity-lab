// Site identity and indexing, shared by the route metadata, robots.txt and the sitemap.
import type { Metadata } from 'next';

export const SITE_URL = 'https://liquidityparadox.netlify.app';
export const SITE_NAME = 'The Liquidity Paradox';
export const REPO_URL = 'https://github.com/VM25/liquidity-lab';

/** Search engines may index only Netlify's production build. Deploy previews, branch deploys and local builds carry
 *  noindex and a disallow-all robots.txt. Netlify sets CONTEXT during its builds; every page is static, so this is read
 *  once, at build time. */
export const INDEXABLE = process.env.CONTEXT === 'production';

/** The share image: the approved home hero (public/og-image.png, 1200 × 630). */
const OG_IMAGE = {
  url: '/og-image.png',
  width: 1200,
  height: 630,
  alt: 'The Liquidity Paradox home page: “We could predict the market. We couldn’t profitably make it.”, beside forecast skill and the trading result at the attainable fee.',
};

export const ROUTES = ['/', '/lab', '/research', '/methods', '/paper'] as const;

/** Metadata for one page: its title and description, the canonical production URL and the matching Open Graph fields. */
export function pageMeta({ path, title, description }: { path: (typeof ROUTES)[number]; title: string; description: string }): Metadata {
  const full = path === '/' ? title : `${title} · ${SITE_NAME}`;
  return {
    title: { absolute: full },
    description,
    alternates: { canonical: path },
    openGraph: { type: 'website', siteName: SITE_NAME, locale: 'en_US', url: path, title: full, description, images: [OG_IMAGE] },
    twitter: { card: 'summary_large_image', title: full, description, images: [OG_IMAGE] },
  };
}
