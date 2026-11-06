import { Layout } from '../../components/Layout';
import { pageMeta } from '../../site';
import Lab from '../../views/Lab';
import '../../styles/lab.css';

export const metadata = pageMeta({
  path: '/lab',
  title: 'Scenario Lab',
  description: 'Every tested combination of policy, fill model, latency and fee schedule from the frozen experiments. Nothing interpolated.',
});

export default function Page() {
  return <Layout page="lab"><Lab /></Layout>;
}
