import axios from 'axios'
import { ElMessage } from 'element-plus'

// Create axios instance with base configuration
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // You can add auth tokens here if needed in the future
    // config.headers.Authorization = `Bearer ${token}`
    return config
  },
  (error) => {
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    // Handle errors globally
    const message = error.response?.data?.detail || error.message || 'An error occurred'

    // Show error message to user
    ElMessage.error(message)

    console.error('Response error:', error)
    return Promise.reject(error)
  }
)

export default api
