import noise3 from '../../assets/media/noise3.png';
import eragon from '../../assets/logos/Eragon.svg';
import entelligence from '../../assets/logos/Entelligence.svg';
import micro from '../../assets/logos/Micro.svg';
import hobbes from '../../assets/logos/Hobbes.svg';
import bear from '../../assets/logos/Bear.svg';
import scaleAgentic from '../../assets/logos/ScaleAgentic.svg';
import virio from '../../assets/logos/Virio.svg';
import superMe from '../../assets/logos/SuperMe.svg';

const logos = [
  { name: 'Eragon', src: eragon },
  { name: 'Entelligence AI', src: entelligence },
  { name: 'micro', src: micro },
  { name: 'HOBBES', src: hobbes },
  { name: 'Bear', src: bear },
  { name: 'ScaleAgentic', src: scaleAgentic },
  { name: 'Virio', src: virio },
  { name: 'SuperMe', src: superMe }
];

function LogoCell({ logo }) {
  return (
    <div className="relative h-12 w-40 flex-shrink-0 mx-4 md:mx-8 grayscale opacity-70 pointer-events-none">
      <img
        src={logo.src}
        alt={logo.name}
        loading="lazy"
        decoding="async"
        className="object-contain"
        style={{ position: 'absolute', height: '100%', width: '100%', left: 0, top: 0, right: 0, bottom: 0, color: 'transparent' }}
      />
    </div>
  );
}

export default function LogoMarquee() {
  // Duplicate the set twice so the marquee can loop seamlessly.
  const track = [...logos, ...logos];
  return (
    <div
      className="marquee-strip relative w-full overflow-hidden border-b border-onyx bg-stone-900 py-6"
      style={{
        backgroundImage: `url(${noise3})`,
        backgroundRepeat: 'repeat',
        backgroundSize: '120px 120px'
      }}
    >
      <div className="marquee-track items-center">
        {track.map((logo, i) => (
          <LogoCell key={`${logo.name}-${i}`} logo={logo} />
        ))}
      </div>
    </div>
  );
}
