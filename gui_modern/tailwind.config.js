/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#0f172a',
        primary: {
          light: '#c084fc',
          DEFAULT: '#a855f7',
          dark: '#9333ea',
        },
        secondary: {
          light: '#2dd4bf',
          DEFAULT: '#14b8a6',
          dark: '#0d9488',
        }
      },
      backdropBlur: {
        xs: '2px',
      }
    },
  },
  plugins: [],
}
