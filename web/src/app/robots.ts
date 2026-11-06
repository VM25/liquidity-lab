import type { MetadataRoute } from 'next';
import { INDEXABLE, SITE_URL } from '../site';

export const dynamic = 'force-static';

// Production allows crawling and points to the sitemap; every other build (deploy previews, branch deploys, local) disallows it.
export default function robots(): MetadataRoute.Robots {
  return INDEXABLE
    ? { rules: { userAgent: '*', allow: '/' }, sitemap: `${SITE_URL}/sitemap.xml` }
    : { rules: { userAgent: '*', disallow: '/' } };
}
