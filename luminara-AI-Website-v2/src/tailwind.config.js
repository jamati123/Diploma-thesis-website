// tailwind.config.js
module.exports = {
    content: [
      "./index.html",
      "./src/**/*.{vue,js,ts,jsx,tsx}",
    ],
    theme: {
      extend: {
        colors: {
          primary: {
            light: '#3b82f6', // Blau
            DEFAULT: '#1e40af',
            dark: '#1e3a8a',
          },
          secondary: {
            light: '#8b5cf6', // Indigo
            DEFAULT: '#6d28d9',
            dark: '#4c1d95',
          },
        },
        animation: {
          'fade-in-down': 'fade-in-down 1s ease-out',
          'fade-in-up': 'fade-in-up 1s ease-out',
          'bounce-slow': 'bounce-slow 3s infinite',
        },
        keyframes: {
          'fade-in-down': {
            '0%': {
              opacity: '0',
              transform: 'translateY(-20px)',
            },
            '100%': {
              opacity: '1',
              transform: 'translateY(0)',
            },
          },
          'fade-in-up': {
            '0%': {
              opacity: '0',
              transform: 'translateY(20px)',
            },
            '100%': {
              opacity: '1',
              transform: 'translateY(0)',
            },
          },
          'bounce-slow': {
            '0%, 100%': {
              transform: 'translateY(0)',
            },
            '50%': {
              transform: 'translateY(-10px)',
            },
          },
        },
      },
    },
    plugins: [
      require('@tailwindcss/typography'), // Füge das Typografie-Plugin hinzu
    ],
  }
  