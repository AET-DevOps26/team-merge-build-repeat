import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import path from 'path'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, '.'),
    },
  },
  server: {
    proxy: {
      '/api/game-engine': {
        target: 'http://localhost:8082',
        rewrite: (path) => path.replace(/^\/api\/game-engine/, ''),
      },
      '/api/genai': {
        target: 'http://localhost:8002',
        rewrite: (path) => path.replace(/^\/api\/genai/, ''),
      },
    },
  },
})
