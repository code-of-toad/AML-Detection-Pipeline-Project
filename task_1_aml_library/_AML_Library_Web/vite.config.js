import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  // Base path for GitHub Pages
  // For GitHub Actions: automatically set via VITE_BASE_PATH env var
  // For local development: defaults to '/'
  // 
  // To manually set for a specific repo:
  // - Repo: 'myusername/aml-library' → base: '/aml-library/'
  // - Repo: 'myusername/myusername.github.io' → base: '/'
  // - Custom domain → base: '/'
  base: process.env.VITE_BASE_PATH || '/',
})
