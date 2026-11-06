import type { MetadataRoute } from 'next';
import { ROUTES, SITE_URL } from '../site';

export const dynamic = 'force-static';

export default function sitemap(): MetadataRoute.Sitemap {
  return ROUTES.map((path) => ({ url: `${SITE_URL}${path === '/' ? '' : path}` }));
}
