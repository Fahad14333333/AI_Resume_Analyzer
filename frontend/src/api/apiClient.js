import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

export const client = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const uploadResume = (formData) => client.post('/v1/upload-resume', formData, {
  headers: {
    'Content-Type': 'multipart/form-data',
  },
})

export const analyzeResume = (payload) => client.post('/v1/analyze', payload)
export const rankResumes = (payload) => client.post('/v1/rank', payload)
export const getHealth = () => client.get('/health')
