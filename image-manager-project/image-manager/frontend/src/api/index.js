import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
})

export const getImages = (page = 1, limit = 20) => 
  api.get('/images/', { params: { page, limit } })

export const uploadImage = (formData, onProgress) => 
  api.post('/images/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress: onProgress
  })

export const deleteImage = (id) => 
  api.delete(`/images/${id}`)