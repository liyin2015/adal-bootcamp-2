import { useState } from 'react';
import wordmark from '../../assets/media/wordmark-light.svg';

function ChevronDown({ className = '' }) {
  return (
    <svg
      className={className}
      viewBox="0 0 12 12"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <path d="M3 4.5 6 7.5 9 4.5" />
    </svg>
  );
}

function HamburgerIcon({ className = '' }) {
  return (
    <svg
      className={className}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <path d="M4 7h16" />
      <path d="M4 12h16" />
      <path d="M4 17h16" />
    </svg>
  );
}

const navLinkClass =
  'uppercase font-body text-[14px] font-normal tracking-[0.7px] text-stone-100 transition-colors';

export default function Navbar() {
  const [open, setOpen] = useState(false);
  return (
    <nav className="sticky top-0 z-50 w-full bg-transparent">
      <div className="mx-auto max-w-screen-xl px-8 xl:px-8 h-[77px] flex items-center justify-between">
        <a href="/" aria-label="Hyperspell home" className="flex items-center">
          <img
            src={wordmark}
            alt="Logo"
            width={128}
            height={32}
            decoding="async"
            className="w-[128px] h-8 translate-y-[4px]"
          />
        </a>

        {/* Desktop nav */}
        <div className="hidden md:flex items-center gap-12">
          <button className={`${navLinkClass} inline-flex items-center gap-2`}>
            Resources
            <ChevronDown className="w-3 h-3" />
          </button>
          <a
            href="https://cal.com/conor-brennan-burke/30-minute"
            className={`${navLinkClass} inline-flex items-center gap-2`}
          >
            Book a demo →
          </a>
        </div>

        {/* Mobile hamburger */}
        <button
          aria-label="Open menu"
          aria-expanded={open}
          onClick={() => setOpen((v) => !v)}
          className="md:hidden inline-flex items-center justify-center text-stone-100 p-2"
        >
          <HamburgerIcon className="w-6 h-6" />
        </button>
      </div>
    </nav>
  );
}
