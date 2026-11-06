import type { Metadata, Viewport } from 'next';
import type { ReactNode } from 'react';
import { SiteEffects } from '../components/SiteEffects';
import { INDEXABLE, SITE_NAME, SITE_URL } from '../site';
import '../fonts';
import '../styles/base.css';

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: SITE_NAME,
  applicationName: SITE_NAME,
  authors: [{ name: 'Vatsal Maniar' }],
  robots: INDEXABLE ? { index: true, follow: true } : { index: false, follow: false },
  icons: { icon: { url: '/favicon.svg', type: 'image/svg+xml' } },
};

export const viewport: Viewport = { width: 'device-width', initialScale: 1, colorScheme: 'light' };

/* One entrance for the home hero, only where it can play: on Home, motion allowed, the tab visible, and once per visit.
   Without this class, or without JavaScript, the hero renders in its final state; the class is removed after the entrance
   either way. It runs in <head>, before the hero is painted. */
const INTRO = `(function () { try {
  if (location.pathname !== '/') return;
  if (matchMedia('(prefers-reduced-motion: reduce)').matches || document.visibilityState !== 'visible') return;
  if (sessionStorage.getItem('lp-intro')) return;
  sessionStorage.setItem('lp-intro', '1');
  var d = document.documentElement; d.classList.add('intro');
  setTimeout(function () { d.classList.remove('intro'); }, 1600);
} catch (e) {} })();`;

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    // the head script and SiteEffects add classes (intro, live) to <html> before and after hydration
    <html lang="en" suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: INTRO }} />
      </head>
      <body>
        {children}
        <SiteEffects />
      </body>
    </html>
  );
}
