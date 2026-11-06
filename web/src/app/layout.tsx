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

/* Runs in <head> while the page is parsed, before React hydrates it.
   1. Netlify's edge inserts a line break and an HTML comment ("This site is hosted on Netlify…") at the top of <head>.
      The line break becomes a whitespace text node that React does not expect there, and hydration fails (React error
      #418). The site renders no text in <head>, so whitespace-only text nodes there are removed.
   2. One entrance for the home hero, only where it can play: on Home, motion allowed, the tab visible, and once per visit.
      Without this class, or without JavaScript, the hero renders in its final state; the class is removed after the
      entrance either way. */
const HEAD_SCRIPT = `(function () { try {
  for (var n = document.head.firstChild, next; n; n = next) {
    next = n.nextSibling;
    if (n.nodeType === 3 && !n.data.trim()) document.head.removeChild(n);
  }
} catch (e) {} })();
(function () { try {
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
        <script dangerouslySetInnerHTML={{ __html: HEAD_SCRIPT }} />
      </head>
      <body>
        {children}
        <SiteEffects />
      </body>
    </html>
  );
}
