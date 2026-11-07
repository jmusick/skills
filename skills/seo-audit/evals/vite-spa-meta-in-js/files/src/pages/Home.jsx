import { usePageMeta } from '../hooks/usePageMeta.js';

export default function Home() {
  usePageMeta({
    title: 'Tidepool | Tide alerts for anglers and kayakers',
    description: 'Tidepool texts you before the tide turns at the beaches you fish and paddle. Free for three locations.',
    image: 'https://tidepool.example/og-home.png',
  });
  return (
    <main>
      <h1>Know when the tide turns</h1>
      <p>Pick your beaches and Tidepool sends a text an hour before high and low tide, with the wind and swell for that spot.</p>
    </main>
  );
}
