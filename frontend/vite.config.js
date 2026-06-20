import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0', // Allow external connections (needed for Docker)
    port: 5173,
    strictPort: true, // Fail if port is already in use
    proxy: {
      // Proxy API requests to backend (optional, for development)
      // '/api': {
      //   target: 'http://localhost:8000',
      //   changeOrigin: true,
      // }
    }
  },
  preview: {
    host: '0.0.0.0',
    port: 5173
  }
})
