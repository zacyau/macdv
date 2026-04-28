import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

export async function queryStock(params) {
  const response = await api.get('/stock/query', { params })
  return response.data
}
