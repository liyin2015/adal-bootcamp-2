import { useEffect, useRef, useState } from 'react';
import Button from '../ui/Button.jsx';
import noise2 from '../../assets/media/noise2.png';

// Hero orb — HERO projectId is `NA0zXCIcHuVGYkLQGQbh` per live-source data.
// Mirrors /Users/li/hyperspell-clone/src/components/UnicornScene.tsx so the
// orb animates autonomously on page load without any mouse input.
const HERO_PROJECT_ID = 'NA0zXCIcHuVGYkLQGQbh';

function UnicornScene() {
  const hostRef = useRef(null);
  const [failed, setFailed] = useState(false);
  const [retried, setRetried] = useState(false);

  useEffect(() => {
    let cancelled = false;
    const start = () => {
      if (cancelled) return;
      const US = window.UnicornStudio;
      if (!US || !hostRef.current) {
        setTimeout(start, 100);
        return;
      }
      try {
        const cfg = {
          element: hostRef.current,
          projectId: HERO_PROJECT_ID,
          fps: 60,
          dpi: 1.5,
          scale: 1,
          lazyLoad: false,
          ariaLabel: 'Scene',
        };
        const ret = US.addScene(cfg);
        if (ret && typeof ret.then === 'function') {
          ret.catch((e) => {
            console.warn('[UnicornScene] addScene rejected:', e);
            if (!retried) {
              setRetried(true);
              try {
                US.addScene({
                  element: hostRef.current,
                  projectId: HERO_PROJECT_ID,
                  ariaLabel: 'Scene',
                });
              } catch {
                setFailed(true);
              }
            } else {
              setFailed(true);
            }
          });
        }
      } catch (e) {
        console.warn('[UnicornScene] threw:', e);
        setFailed(true);
      }
    };
    start();
    return () => {
      cancelled = true;
    };
  }, [retried]);

  if (failed) {
    return (
      <div
        aria-hidden="true"
        className="absolute inset-0"
        style={{
          background:
            'radial-gradient(60% 50% at 65% 50%, lab(70 35 25 / 0.55) 0%, transparent 70%), radial-gradient(40% 30% at 85% 40%, lab(40 60 80 / 0.35) 0%, transparent 60%)',
        }}
      />
    );
  }

  return <div ref={hostRef} className="absolute inset-0" aria-label="Scene" />;
}

export default function Hero() {
  return (
    <section
      className="hero-section relative overflow-hidden border-b border-onyx bg-stone-900"
      style={{
        backgroundImage: `url(${noise2})`,
        backgroundRepeat: 'repeat',
        backgroundSize: '120px 120px'
      }}
    >
      {/* z-0: Unicorn Studio WebGL layer (live embed). Matches the reference
          wrapper: no pointer-events-none (the orb is mouse-driven and the CTA
          sits on a sibling z-10 layer so it remains clickable regardless). */}
      <div className="absolute inset-0 w-full h-full">
        <UnicornScene />
      </div>

      {/* z-10: hero content */}
      <div className="mx-auto relative z-10 px-8 xl:px-8 py-12 md:py-20 max-w-screen-xl">
        <h1
          className="mb-6 text-stone-100 w-full md:w-3/5 font-display text-[3rem] md:text-[4rem]"
          style={{
            fontWeight: 400,
            lineHeight: '70.4px',
            letterSpacing: '-3.84px',
            color: '#D6D6D6'
          }}
        >
          A brain for your company.
        </h1>
        <p
          className="font-body mb-12 text-stone-100 max-w-3xl"
          style={{
            fontWeight: 400,
            fontSize: '30px',
            lineHeight: '36px',
            letterSpacing: '-0.72px',
            color: '#D6D6D6'
          }}
        >
          Hyperspell connects your tools, builds a context graph, and surfaces it as a filesystem any agent can read.
        </p>
        <div className="flex flex-col md:flex-row mb-12 gap-6">
          <Button href="https://cal.com/conor-brennan-burke/30-minute">Book a demo</Button>
        </div>
      </div>
    </section>
  );
}