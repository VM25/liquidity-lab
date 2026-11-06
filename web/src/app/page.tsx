import { Layout } from '../components/Layout';
import { pageMeta } from '../site';
import Overview from '../views/Overview';
import '../styles/home.css';

export const metadata = pageMeta({
  path: '/',
  title: 'The Liquidity Paradox',
  description: 'Pre-registered research on Binance SOLUSDT: short-horizon order-book forecasts had real skill, yet every passive quoting rule tested lost money at the attainable fee.',
});

export default function Page() {
  return <Layout page="overview"><Overview /></Layout>;
}
