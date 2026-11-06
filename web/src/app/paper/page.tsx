import { Layout } from '../../components/Layout';
import { pageMeta } from '../../site';
import Paper from '../../views/Paper';
import '../../styles/pages.css';

export const metadata = pageMeta({
  path: '/paper',
  title: 'Paper & Code',
  description: 'The frozen research paper, reproducibility supplement, checksums and reproduction steps.',
});

export default function Page() {
  return <Layout page="paper"><Paper /></Layout>;
}
