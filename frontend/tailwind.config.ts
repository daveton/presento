import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // 品牌色
        'st-primary': '#4D77FF',
        'st-primary-press': '#3D66FF',
        'st-primary-soft': '#E0E7FF',
        'st-primary-highlight': '#6B8FFF',
        // 背景
        'st-bg': '#F5F7FF',
        'st-bg-soft': '#EEF2FF',
        'st-surface': '#FFFFFF',
        'st-surface-accent': '#F0F4FF',
        // 边框
        'st-border': '#E2E8F0',
        // 文本
        'st-text': '#1E293B',
        'st-text-sub': '#475569',
        'st-text-muted': '#94A3B8',
        'st-placeholder': '#CBD5E1',
        // 状态
        'st-success': '#3DA86E',
        'st-success-soft': '#E7F6EE',
        'st-warning': '#D98A20',
        'st-warning-soft': '#FFF2D8',
        'st-risk': '#E5484D',
        'st-risk-soft': '#FDECEC',
        // 金色
        'st-gold': '#FF9800',
      },
      borderRadius: {
        'st-sm': '16px',
        'st-md': '24px',
        'st-lg': '32px',
        'st-xl': '40px',
      },
      boxShadow: {
        'st-soft': '0 4px 18px rgba(30, 41, 59, 0.04)',
        'st-card': '0 12px 36px rgba(77, 119, 255, 0.10)',
        'st-float': '0 16px 48px rgba(30, 41, 59, 0.14)',
        'st-button': '0 8px 20px rgba(77, 119, 255, 0.30)',
      },
    },
  },
  plugins: [],
}

export default config
