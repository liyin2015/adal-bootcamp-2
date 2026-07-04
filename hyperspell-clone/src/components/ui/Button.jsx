export default function Button({ children, href = 'https://cal.com/conor-brennan-burke/30-minute', className = '' }) {
  const baseStyle = {
    background:
      'linear-gradient(to right, lab(57.9249 57.5686 25.3116 / 0.8) 0%, lab(68.2299 49.5438 29.1709 / 0.8) 50%, lab(75.4697 25.3835 45.1166 / 0.8) 100%)',
    boxShadow:
      'rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, lab(0 0 0 / 0.2) 0px 10px 15px -3px, lab(0 0 0 / 0.2) 0px 4px 6px -4px'
  };
  return (
    <a
      href={href}
      className={
        'inline-block border border-stone-50 text-stone-50 text-center ' +
        'pt-4 pb-3.5 px-8 transition-all duration-300 ease-in-out ' +
        'backdrop-blur-xs cursor-pointer text-2xl font-body ' +
        'w-full md:w-[288px] md:h-[64px] ' +
        className
      }
      style={baseStyle}
    >
      {children}
    </a>
  );
}
