import { usePageMeta } from '../hooks/usePageMeta.js';

export default function Pricing() {
  usePageMeta({
    title: 'Pricing | Tidepool',
    description: 'Tidepool is free for three locations. Pro is $4 a month for unlimited locations and swell forecasts.',
  });
  return (
    <main>
      <h1>Pricing</h1>
      <p>Free: three locations. Pro: $4 a month for unlimited locations and swell forecasts.</p>
    </main>
  );
}
