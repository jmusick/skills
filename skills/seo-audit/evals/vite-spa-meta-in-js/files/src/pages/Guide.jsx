import { usePageMeta } from '../hooks/usePageMeta.js';

export default function Guide() {
  usePageMeta({
    title: 'How to Read a Tide Table | Tidepool',
    description: 'What high water, low water, and tidal range mean, and how to plan a fishing or kayaking trip around them.',
  });
  return (
    <main>
      <h1>How to read a tide table</h1>
      <p>A tide table lists the times and heights of high and low water for one station.</p>
    </main>
  );
}
