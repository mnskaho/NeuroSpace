/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        mono: ['JetBrains Mono', 'monospace'],
        sans: ['Manrope', 'sans-serif'],
      },
      colors: {
        space: {
          DEFAULT: '#0A0F1E',
          2: '#0D1428',
          3: '#111827',
        },
        panel: {
          DEFAULT: '#131B2E',
          2: '#1A2540',
          3: '#1E2D4A',
        },
        quantum: {
          purple: '#7C3AED',
          cyan: '#06B6D4',
          teal: '#10CFAA',
          pink: '#EC4899',
          violet: '#A78BFA',
        },
        text: {
          primary: '#F0F4FF',
          secondary: '#8B9CC8',
          muted: '#4B5A7A',
        },
      },
      backgroundImage: {
        'gradient-quantum': 'linear-gradient(135deg, #7C3AED 0%, #06B6D4 50%, #10CFAA 100%)',
        'gradient-hero': 'linear-gradient(160deg, #0A0F1E 0%, #0D1428 40%, #111827 100%)',
        'gradient-card': 'linear-gradient(135deg, rgba(124,58,237,0.1), rgba(6,182,212,0.05))',
      },
      animation: {
        'float': 'float 4s ease-in-out infinite',
        'float-delayed': 'float-delayed 5s ease-in-out 1s infinite',
        'pulse-glow': 'pulse-glow 2s ease-in-out infinite',
        'fadeInUp': 'fadeInUp 0.8s cubic-bezier(0.22, 1, 0.36, 1) forwards',
        'blink': 'blink 1s step-end infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-12px)' },
        },
        'float-delayed': {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-8px)' },
        },
        'pulse-glow': {
          '0%, 100%': { opacity: '0.4' },
          '50%': { opacity: '1' },
        },
        fadeInUp: {
          from: { opacity: '0', transform: 'translateY(30px)' },
          to: { opacity: '1', transform: 'translateY(0)' },
        },
        blink: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0' },
        },
      },
      boxShadow: {
        'glow-purple': '0 0 30px rgba(124, 58, 237, 0.3)',
        'glow-cyan': '0 0 30px rgba(6, 182, 212, 0.3)',
        'card': '0 8px 32px rgba(0, 0, 0, 0.4)',
      },
      backdropBlur: {
        xs: '2px',
      },
    },
  },
  plugins: [],
};