/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        minvuBlue: '#0b4f99',
        minvuLight: '#e8f1fb',
      },
    },
  },
  plugins: [],
}
