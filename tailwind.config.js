/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/templates/**/*.html",   // 👈 Flask templates
    "./app/**/*.py",   
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

