import Navbar from './components/layout/Navbar.jsx';
import Hero from './components/sections/Hero.jsx';
import LogoMarquee from './components/sections/LogoMarquee.jsx';

export default function App() {
  return (
    <div className="min-h-screen bg-stone-900 text-stone-100 font-body">
      <Navbar />
      <Hero />
      <LogoMarquee />
    </div>
  );
}
