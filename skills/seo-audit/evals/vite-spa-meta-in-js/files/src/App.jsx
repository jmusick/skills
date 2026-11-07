import { Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home.jsx';
import Pricing from './pages/Pricing.jsx';
import Guide from './pages/Guide.jsx';

export default function App() {
  return (
    <>
      <nav>
        <Link to="/">Tidepool</Link> <Link to="/pricing">Pricing</Link> <Link to="/guides/tide-tables">Tide table guide</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/pricing" element={<Pricing />} />
        <Route path="/guides/tide-tables" element={<Guide />} />
      </Routes>
    </>
  );
}
