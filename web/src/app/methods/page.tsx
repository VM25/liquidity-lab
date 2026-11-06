import { Layout } from '../../components/Layout';
import { pageMeta } from '../../site';
import Methods from '../../views/Methods';
import '../../styles/katex.css';
import '../../styles/pages.css';

export const metadata = pageMeta({
  path: '/methods',
  title: 'Methods & Data',
  description: 'Study design, sample, execution model, equations, inference, limitations and data sources.',
});

export default function Page() {
  return <Layout page="methods"><Methods /></Layout>;
}
