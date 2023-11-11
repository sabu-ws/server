/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "../templates/*.html",
    "../**/templates/*.html",
    "./node_modules/flowbite/**/*.js"
  ],
  theme: {
    extend: { 
      spacing: {
        '128': '34rem',
        '160': '40rem',
      }},
  },
  fontFamily: {
    'body': [
  'Lato', 
  'ui-sans-serif', 
  'system-ui', 
  '-apple-system', 
  'system-ui', 
  'Segoe UI', 
  'Roboto', 
  'Helvetica Neue', 
  'Arial', 
  'Noto Sans', 
  'sans-serif', 
  'Apple Color Emoji', 
  'Segoe UI Emoji', 
  'Segoe UI Symbol', 
  'Noto Color Emoji'
],
    'sans': [
  'Lato', 
  'ui-sans-serif', 
  'system-ui', 
  '-apple-system', 
  'system-ui', 
  'Segoe UI', 
  'Roboto', 
  'Helvetica Neue', 
  'Arial', 
  'Noto Sans', 
  'sans-serif', 
  'Apple Color Emoji', 
  'Segoe UI Emoji', 
  'Segoe UI Symbol', 
  'Noto Color Emoji'
]
  },
  plugins: [
    require('flowbite/plugin')({
      charts: true,
    })
  ],
  darkMode: 'class',
  
}

