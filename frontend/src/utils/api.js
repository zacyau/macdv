import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 60000
})

export async function queryStock(params) {
  const response = await api.get('/stock/query', { params })
  return response.data
}

export async function batchQueryStock(queries) {
  const response = await api.post('/stock/batch_query', queries)
  return response.data
}
