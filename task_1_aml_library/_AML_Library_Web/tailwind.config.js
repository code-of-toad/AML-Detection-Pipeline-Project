/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#e8f0fe',
          100: '#d1e1fd',
          200: '#a3c3fb',
          300: '#75a5f9',
          400: '#5e96e8',
          500: '#4a89dc',
          600: '#3d6fb8',
          700: '#305594',
          800: '#233b70',
          900: '#16214c',
        },
      },
    },
  },
  plugins: [],
}
