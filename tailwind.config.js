// tailwind.config.js

module.exports = {
  content: [
    './templates/**/*.html',
    './static/**/*.css',
    './devsearchey/**/*.py',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#4f46e5',
          dark: '#3730a3',
        },
        secondary: {
          DEFAULT: '#ec4899',
          dark: '#be185d',
        },
        accent: {
          DEFAULT: '#22c55e',
          dark: '#15803d',
        },
      },
      fontFamily: {
        sans: ['Poppins', 'Arial', 'sans-serif'],
      },
      backgroundImage: theme => ({
        'hero-pattern': "url('/static/images/hero-bg.jpg')",
      }),
      animation: {
        'fade-in': 'fadeIn 1s ease-in forwards',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: 0 },
          '100%': { opacity: 1 },
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('@tailwindcss/forms'),
  ],
}