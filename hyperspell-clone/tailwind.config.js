/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      fontFamily: {
        display: ['exposure', 'serif'],
        body: ['Geist', 'system-ui', 'sans-serif']
      },
      colors: {
        stone: {
          50: '#E9E9E9',
          100: '#D6D6D6',
          900: '#161010'
        },
        onyx: '#171717'
      },
      maxWidth: {
        'screen-xl': '1280px'
      }
    }
  },
  plugins: []
};
