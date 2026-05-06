/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#eff4fb',
          100: '#d9e4f2',
          200: '#b3c9e5',
          300: '#8daed8',
          400: '#6793cb',
          500: '#4178be',
          600: '#34619e',
          700: '#274a7e',
          800: '#1a335e',
          900: '#0d1c3e',
        }
      }
    },
  },
  plugins: [],
}
