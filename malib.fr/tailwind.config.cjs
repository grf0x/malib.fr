/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ['./src/**/*.{html,js,svelte,css}'],
    theme: {
      extend: {  
        fontFamily: {
          'malib': ['"malib"', 'serif'], 
          'futural': ['"futural"', 'sans-serif'], 
          'futurar': ['"futurar"', 'sans-serif']
        },  
        backgroundImage: {
          'welcome': "url('/imgs/bg.jpg')",
        },  
        colors: {
        'custom-grey': 'rgb(241,241,241)',
        'custom-red': 'rgb(215,120,120)',
        'custom-red-dark': 'rgb(207,92,92)',
        'custom-red-light': 'rgb(221,139,139)',
      },}
    },
    variants: ["hover", "responsive", "focus", "focus-within"],
    plugins: [],
}
