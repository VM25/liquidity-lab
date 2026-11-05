import { renderToString } from 'react-dom/server';
import { Layout, type PageId } from './components/Layout';
import Lab from './pages/Lab';
import Methods from './pages/Methods';
import Overview from './pages/Overview';
import Paper from './pages/Paper';
import Research from './pages/Research';

const PAGES = { overview: Overview, research: Research, lab: Lab, methods: Methods, paper: Paper };

export function render(page: PageId): string {
  const P = PAGES[page];
  return renderToString(<Layout page={page}><P /></Layout>);
}
