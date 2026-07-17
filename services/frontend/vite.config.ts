import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import path from 'path'

const isDocker = process.env.DOCKER_ENV === 'true'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, '.'),
    },
  },
  server: {
    proxy: {
      '/application': {
        target: isDocker ? 'http://application:8080' : 'http://localhost:8081',
        rewrite: (path) => path.replace(/^\/application/, ''),
      },
      '/game-engine': {
        target: isDocker ? 'http://game-engine:8080' : 'http://localhost:8082',
        rewrite: (path) => path.replace(/^\/game-engine/, ''),
      },
      '/genai': {
        target: isDocker ? 'http://genai:8080' : 'http://localhost:8002',
        rewrite: (path) => path.replace(/^\/genai/, ''),
      },
      '/chat': {
        target: isDocker ? 'http://chat:8080' : 'http://localhost:8083',
        rewrite: (path) => path.replace(/^\/chat/, ''),
      },
    },
  },
})
