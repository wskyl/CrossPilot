/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#1677ff',
        secondary: '#722ed1',
      },
    },
  },
  plugins: [],
  corePlugins: {
    preflight: false, // Disable preflight to avoid conflicts with Ant Design
  },
}
