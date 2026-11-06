import { Layout } from '../../components/Layout';
import { pageMeta } from '../../site';
import Research from '../../views/Research';
import '../../styles/pages.css';

export const metadata = pageMeta({
  path: '/research',
  title: 'Research',
  description: 'Experiments E001 to E004 with discovery intervals, held-out values and the full per-experiment label table.',
});

export default function Page() {
  return <Layout page="research"><Research /></Layout>;
}
